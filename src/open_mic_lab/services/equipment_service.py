"""Deterministic Chapter 8 signal-flow services."""

from dataclasses import dataclass, replace

from open_mic_lab.domain.equipment import (
    Connection,
    NodeRole,
    OutputRole,
    SignalNode,
    SignalPath,
    SignalPort,
    SignalType,
)


@dataclass(frozen=True, slots=True)
class SignalObservation:
    """Structured learner-facing observation from signal analysis."""

    severity: str
    code: str
    message: str
    node_identifier: str = ""
    connection_identifier: str = ""


@dataclass(frozen=True, slots=True)
class SignalFlowAnalysis:
    """Analysis of a complete signal graph."""

    path_identifier: str
    end_to_end_paths: tuple[tuple[str, ...], ...]
    disconnected_components: tuple[str, ...]
    missing_connections: tuple[str, ...]
    incompatible_connections: tuple[str, ...]
    unused_equipment: tuple[str, ...]
    monitor_routes: tuple[tuple[str, ...], ...]
    performer_outputs: tuple[str, ...]
    audience_outputs: tuple[str, ...]
    observations: tuple[SignalObservation, ...]


@dataclass(frozen=True, slots=True)
class SignalFlowComparison:
    """Before/after comparison for equipment experiments."""

    original_identifier: str
    changed_identifier: str
    differences: tuple[str, ...]


class SignalFlowService:
    """Analyze and visualize live-sound signal paths deterministically."""

    def analyze(self, signal_path: SignalPath) -> SignalFlowAnalysis:
        """Return structured observations about the connected graph."""
        nodes = {node.identifier: node for node in signal_path.nodes}
        outgoing: dict[str, list[Connection]] = {node.identifier: [] for node in signal_path.nodes}
        incoming: dict[str, list[Connection]] = {node.identifier: [] for node in signal_path.nodes}
        observations: list[SignalObservation] = []
        incompatible: list[str] = []
        missing: list[str] = []
        for connection in signal_path.connections:
            if connection.source_node not in nodes or connection.destination_node not in nodes:
                missing.append(connection.identifier)
                observations.append(
                    SignalObservation(
                        "error",
                        "missing-node",
                        "Connection references equipment that is not in the setup.",
                        connection_identifier=connection.identifier,
                    )
                )
                continue
            outgoing[connection.source_node].append(connection)
            incoming[connection.destination_node].append(connection)
            source_port = self._port(
                nodes[connection.source_node].outputs, connection.source_output
            )
            dest_port = self._port(
                nodes[connection.destination_node].inputs, connection.destination_input
            )
            if source_port is None or dest_port is None:
                incompatible.append(connection.identifier)
                observations.append(
                    SignalObservation(
                        "error",
                        "missing-port",
                        "Connection references an input or output that does not exist.",
                        connection_identifier=connection.identifier,
                    )
                )
            elif not self._compatible(
                source_port.signal_type, dest_port.signal_type, connection.cable.signal_type
            ):
                incompatible.append(connection.identifier)
                observations.append(
                    SignalObservation(
                        "error",
                        "incompatible-signal",
                        f"{nodes[connection.source_node].label} sends "
                        f"{source_port.signal_type.value}, but "
                        f"{nodes[connection.destination_node].label} expects "
                        f"{dest_port.signal_type.value}.",
                        connection_identifier=connection.identifier,
                    )
                )
        roots = tuple(
            n.identifier
            for n in signal_path.nodes
            if n.role
            in {
                NodeRole.AUDIO_SOURCE,
                NodeRole.MICROPHONE,
                NodeRole.INSTRUMENT_OUTPUT,
                NodeRole.PICKUP,
            }
        )
        terminal_paths = tuple(
            sorted(path for root in roots for path in self._walk(root, outgoing, (root,)))
        )
        connected = {item for path in terminal_paths for item in path}
        disconnected = tuple(
            sorted(n.identifier for n in signal_path.nodes if n.identifier not in connected)
        )
        unused = tuple(
            sorted(
                n.identifier
                for n in signal_path.nodes
                if not outgoing[n.identifier]
                and nodes[n.identifier].output_role is OutputRole.INTERNAL
            )
        )
        for node in signal_path.nodes:
            if node.inputs and not incoming[node.identifier]:
                missing.append(node.identifier)
                observations.append(
                    SignalObservation(
                        "warning",
                        "unfed-input",
                        f"{node.label} has no incoming signal, so its role is not heard.",
                        node.identifier,
                    )
                )
            if (
                node.outputs
                and not outgoing[node.identifier]
                and node.output_role is OutputRole.INTERNAL
            ):
                observations.append(
                    SignalObservation(
                        "warning",
                        "unused-output",
                        f"{node.label} has an output with no destination.",
                        node.identifier,
                    )
                )
        if self._has_cycle(outgoing):
            observations.append(
                SignalObservation(
                    "error",
                    "circular-routing",
                    "The setup contains circular routing; sound can feed back into "
                    "earlier equipment.",
                )
            )
        audience = tuple(
            sorted(
                n.label
                for n in signal_path.nodes
                if n.output_role is OutputRole.AUDIENCE and incoming[n.identifier]
            )
        )
        performer = tuple(
            sorted(
                n.label
                for n in signal_path.nodes
                if n.output_role is OutputRole.PERFORMER and incoming[n.identifier]
            )
        )
        monitor_routes = tuple(
            path
            for path in terminal_paths
            if path[-1]
            in {n.identifier for n in signal_path.nodes if n.output_role is OutputRole.PERFORMER}
        )
        if not audience:
            observations.append(
                SignalObservation(
                    "error",
                    "no-audience-output",
                    "No connected audience speaker output is present.",
                )
            )
        return SignalFlowAnalysis(
            signal_path.identifier,
            terminal_paths,
            disconnected,
            tuple(sorted(set(missing))),
            tuple(sorted(set(incompatible))),
            unused,
            monitor_routes,
            performer,
            audience,
            tuple(observations),
        )

    def visualize(self, signal_path: SignalPath) -> str:
        """Create a deterministic text diagram from sources to destinations."""
        nodes = {node.identifier: node for node in signal_path.nodes}
        outgoing: dict[str, list[Connection]] = {node.identifier: [] for node in signal_path.nodes}
        for connection in sorted(signal_path.connections, key=lambda c: c.identifier):
            if connection.source_node in outgoing:
                outgoing[connection.source_node].append(connection)
        roots = [
            n.identifier
            for n in signal_path.nodes
            if not any(c.destination_node == n.identifier for c in signal_path.connections)
        ]
        lines: list[str] = []
        for root in sorted(roots):
            self._draw(root, nodes, outgoing, lines, "", set())
        return "\n".join(lines)

    def compare(self, original: SignalPath, changed: SignalPath) -> SignalFlowComparison:
        """Compare analyses without judging one setup as universally better."""
        left = self.analyze(original)
        right = self.analyze(changed)
        differences = (
            f"Audience outputs changed from {len(left.audience_outputs)} "
            f"to {len(right.audience_outputs)}.",
            f"Performer monitor outputs changed from {len(left.performer_outputs)} "
            f"to {len(right.performer_outputs)}.",
            f"Issue observations changed from {len(left.observations)} "
            f"to {len(right.observations)}.",
            f"End-to-end paths changed from {len(left.end_to_end_paths)} "
            f"to {len(right.end_to_end_paths)}.",
        )
        return SignalFlowComparison(original.identifier, changed.identifier, differences)

    def _walk(
        self,
        node_id: str,
        outgoing: dict[str, list[Connection]],
        path: tuple[str, ...],
    ) -> tuple[tuple[str, ...], ...]:
        if not outgoing.get(node_id):
            return (path,)
        paths: list[tuple[str, ...]] = []
        for connection in sorted(outgoing[node_id], key=lambda c: c.identifier):
            if connection.destination_node in path:
                paths.append(path + (connection.destination_node,))
            else:
                paths.extend(
                    self._walk(
                        connection.destination_node,
                        outgoing,
                        path + (connection.destination_node,),
                    )
                )
        return tuple(paths)

    def _draw(
        self,
        node_id: str,
        nodes: dict[str, SignalNode],
        outgoing: dict[str, list[Connection]],
        lines: list[str],
        prefix: str,
        seen: set[str],
    ) -> None:
        label = nodes[node_id].label if node_id in nodes else node_id
        lines.append(f"{prefix}{label}")
        if node_id in seen:
            lines.append(f"{prefix}  ↺ circular route")
            return
        next_connections = sorted(outgoing.get(node_id, ()), key=lambda c: c.identifier)
        for index, connection in enumerate(next_connections):
            branch = "└──► " if index == len(next_connections) - 1 else "├──► "
            self._draw(
                connection.destination_node,
                nodes,
                outgoing,
                lines,
                prefix + branch,
                seen | {node_id},
            )

    def _port(self, ports: tuple[SignalPort, ...], identifier: str) -> SignalPort | None:
        return next((port for port in ports if port.identifier == identifier), None)

    def _compatible(self, source: SignalType, destination: SignalType, cable: SignalType) -> bool:
        return source is destination and cable is source

    def _has_cycle(self, outgoing: dict[str, list[Connection]]) -> bool:
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> bool:
            if node in visiting:
                return True
            if node in visited:
                return False
            visiting.add(node)
            for connection in outgoing.get(node, ()):
                if visit(connection.destination_node):
                    return True
            visiting.remove(node)
            visited.add(node)
            return False

        return any(visit(node) for node in outgoing)


class EquipmentExperimentService:
    """Immutable equipment experiments."""

    def disconnect_cable(self, signal_path: SignalPath, connection_identifier: str) -> SignalPath:
        """Return a copy with one connection removed."""
        return replace(
            signal_path,
            identifier=f"{signal_path.identifier}-disconnect-{connection_identifier}",
            connections=tuple(
                c for c in signal_path.connections if c.identifier != connection_identifier
            ),
        )

    def add_monitor(
        self, signal_path: SignalPath, monitor: SignalNode, connection: Connection
    ) -> SignalPath:
        """Return a copy with a performer monitor route added."""
        return replace(
            signal_path,
            identifier=f"{signal_path.identifier}-monitor",
            nodes=signal_path.nodes + (monitor,),
            connections=signal_path.connections + (connection,),
        )

    def bypass_pedal(self, signal_path: SignalPath, pedal_identifier: str) -> SignalPath:
        """Return a copy with an effects processor removed from the graph."""
        return replace(
            signal_path,
            identifier=f"{signal_path.identifier}-bypass-{pedal_identifier}",
            connections=tuple(
                c
                for c in signal_path.connections
                if c.source_node != pedal_identifier and c.destination_node != pedal_identifier
            ),
        )

    def replace_node(
        self, signal_path: SignalPath, old_identifier: str, new_node: SignalNode
    ) -> SignalPath:
        """Return a copy with conceptually equivalent equipment swapped in."""
        return replace(
            signal_path,
            identifier=f"{signal_path.identifier}-replace-{old_identifier}",
            nodes=tuple(
                new_node if n.identifier == old_identifier else n for n in signal_path.nodes
            ),
        )
