"""Deterministic analytics for Chapter 15 continuous improvement."""

from dataclasses import replace

from open_mic_lab.domain import (
    AnalyticsReport,
    ImprovementPlan,
    ImprovementRecommendation,
    PerformanceDashboard,
    PerformanceHistory,
    PracticeTrend,
    RepertoireTrend,
    TrendObservation,
)


class PerformanceAnalyticsService:
    """Aggregate performance snapshots into educational trends."""

    def practice_trend(self, history: PerformanceHistory) -> PracticeTrend:
        """Summarize practice consistency without grading the performer."""
        minutes = tuple(snapshot.practice_minutes for snapshot in history.snapshots)
        average = sum(minutes) // len(minutes)
        spread = max(minutes) - min(minutes)
        score = max(0, min(100, 100 - spread))
        observation = (
            "Practice preparation is steady."
            if spread <= 20
            else "Practice time varies across performances."
        )
        return PracticeTrend(average, score, observation)

    def repertoire_trend(self, history: PerformanceHistory) -> RepertoireTrend:
        """Summarize repertoire growth and genre balance."""
        start = history.snapshots[0].repertoire_size
        end = history.snapshots[-1].repertoire_size
        genres = max(snapshot.genre_count for snapshot in history.snapshots)
        if end > start:
            observation = f"Repertoire expanded by {end - start} prepared versions."
        else:
            observation = "Repertoire size stayed stable; maintenance may be the current focus."
        return RepertoireTrend(start, end, genres, observation)

    def trends(self, history: PerformanceHistory) -> tuple[TrendObservation, ...]:
        """Generate readable trends from the first and latest snapshots."""
        first = history.snapshots[0]
        latest = history.snapshots[-1]
        return (
            self._change(
                "Readiness over time", first.readiness_score, latest.readiness_score, "points"
            ),
            self._change(
                "Coordination improvements",
                first.coordination_score,
                latest.coordination_score,
                "points",
            ),
            self._change(
                "Stage communication observations",
                first.communication_score,
                latest.communication_score,
                "points",
            ),
            TrendObservation(
                "Audience observations",
                "summarized",
                (
                    f"{sum(len(s.audience_observations) for s in history.snapshots)} "
                    f"observations collected across {len(history.snapshots)} performances."
                ),
            ),
            TrendObservation(
                "Common recovery scenarios",
                "tracked",
                f"{sum(s.recovery_events for s in history.snapshots)} recovery events documented.",
            ),
            TrendObservation(
                "Original music integration",
                "tracked",
                f"Latest performance included {latest.original_songs} original song(s).",
            ),
            TrendObservation(
                "Event summaries",
                "summarized",
                latest.event_summary,
            ),
        )

    def dashboard(self, history: PerformanceHistory) -> PerformanceDashboard:
        """Create a deterministic text dashboard with block bars."""
        latest = history.snapshots[-1]
        practice = self.practice_trend(history)
        diversity = min(100, latest.genre_count * 18)
        technical = max(0, 100 - (latest.equipment_issues * 15) - (latest.soundcheck_warnings * 10))
        recovery = max(0, min(100, 85 - latest.recovery_events * 8))
        rows = (
            ("Readiness", latest.readiness_score),
            ("Repertoire Diversity", diversity),
            ("Practice Consistency", practice.consistency_score),
            ("Communication", latest.communication_score),
            ("Technical Preparation", technical),
            ("Recovery Confidence", recovery),
        )
        text = "Performance Dashboard\n" + "\n".join(
            f"{name}\n{self._bar(value)}" for name, value in rows
        )
        mermaid = (
            "flowchart TD\n"
            "    History[Performance History] --> Trends[Educational Trends]\n"
            "    Trends --> Dashboard[Text Dashboard]\n"
            "    Trends --> Plan[Improvement Plan]\n"
        )
        return PerformanceDashboard(
            latest.readiness_score,
            diversity,
            practice.consistency_score,
            latest.communication_score,
            technical,
            recovery,
            text,
            mermaid,
        )

    def recommendations(self, history: PerformanceHistory) -> tuple[ImprovementRecommendation, ...]:
        """Generate transparent next actions from trends."""
        latest = history.snapshots[-1]
        practice = self.practice_trend(history)
        repertoire = self.repertoire_trend(history)
        recommendations: list[ImprovementRecommendation] = []
        if latest.readiness_score < 85:
            recommendations.append(
                ImprovementRecommendation(
                    "Increase practice on two developing songs.",
                    (
                        f"Latest readiness is {latest.readiness_score}/100, "
                        "below the 85 target used in sample repertoire."
                    ),
                    ("0", "2", "6"),
                )
            )
        if repertoire.genre_count < 5:
            recommendations.append(
                ImprovementRecommendation(
                    "Expand repertoire into another genre.",
                    (
                        f"History shows {repertoire.genre_count} genres; "
                        "another genre would broaden set options."
                    ),
                    ("1", "2", "3"),
                )
            )
        if practice.consistency_score < 85:
            recommendations.append(
                ImprovementRecommendation(
                    "Stabilize weekly practice before the next performance.",
                    practice.observation,
                    ("6",),
                )
            )
        if latest.communication_score < 80:
            recommendations.append(
                ImprovementRecommendation(
                    "Rehearse transitions and spoken introductions.",
                    (
                        f"Latest communication score is {latest.communication_score}/100 "
                        "in the educational model."
                    ),
                    ("7", "10"),
                )
            )
        if latest.equipment_issues or latest.soundcheck_warnings:
            recommendations.append(
                ImprovementRecommendation(
                    "Improve monitor setup consistency.",
                    (
                        f"Latest snapshot has {latest.equipment_issues} equipment issue(s) "
                        f"and {latest.soundcheck_warnings} sound-check warning(s)."
                    ),
                    ("8", "9"),
                )
            )
        if latest.original_songs < 1:
            recommendations.append(
                ImprovementRecommendation(
                    "Introduce one additional original song.",
                    "No original song appeared in the latest snapshot.",
                    ("13",),
                )
            )
        recommendations.append(
            ImprovementRecommendation(
                "Build a stronger closing repertoire.",
                (
                    "The capstone report always asks whether the final song supports "
                    "the intended listener memory."
                ),
                ("3", "14", "15"),
            )
        )
        return tuple(recommendations)

    def improvement_plan(
        self, history: PerformanceHistory, focus: str = "balanced"
    ) -> ImprovementPlan:
        """Create the baseline improvement plan."""
        recs = self.recommendations(history)
        return ImprovementPlan(
            f"plan-{focus}",
            focus,
            tuple(rec.action for rec in recs[:4]),
            tuple(rec.reason for rec in recs[:4]),
        )

    def report(self, history: PerformanceHistory) -> AnalyticsReport:
        """Build the complete Volume I analytics report."""
        volume_summary = (
            (
                "Repertoire, readiness, arrangements, practice, coordination, communication, "
                "equipment, sound check, audience, recovery, improvisation, originals, and "
                "event orchestration all contribute evidence."
            ),
            (
                "The report summarizes observations across performances and never evaluates "
                "artistic worth."
            ),
            "Recommended next actions are hypotheses for the next learning cycle.",
        )
        return AnalyticsReport(
            history,
            self.practice_trend(history),
            self.repertoire_trend(history),
            self.trends(history),
            self.dashboard(history),
            self.recommendations(history),
            self.improvement_plan(history),
            volume_summary,
        )

    def _change(self, name: str, first: int, latest: int, unit: str) -> TrendObservation:
        delta = latest - first
        direction = "improving" if delta > 0 else "stable" if delta == 0 else "developing"
        return TrendObservation(name, direction, f"Changed from {first} to {latest} {unit}.")

    def _bar(self, value: int) -> str:
        filled = max(0, min(10, round(value / 10)))
        return "█" * filled + "░" * (10 - filled)


class ImprovementExperimentService:
    """Immutable experiments for continuous-improvement plans."""

    def emphasize_practice(self, plan: ImprovementPlan) -> ImprovementPlan:
        """Return a copy focused on deliberate practice."""
        return self._with_focus(
            plan, "practice emphasis", "Schedule two focused practice blocks for developing songs."
        )

    def emphasize_new_repertoire(self, plan: ImprovementPlan) -> ImprovementPlan:
        """Return a copy focused on repertoire expansion."""
        return self._with_focus(
            plan, "new repertoire emphasis", "Add one contrasting genre candidate."
        )

    def emphasize_communication(self, plan: ImprovementPlan) -> ImprovementPlan:
        """Return a copy focused on stage communication."""
        return self._with_focus(
            plan, "communication emphasis", "Rehearse concise introductions and transitions aloud."
        )

    def prepare_for_upcoming_performance(self, plan: ImprovementPlan) -> ImprovementPlan:
        """Return a copy focused on near-term performance readiness."""
        return self._with_focus(
            plan, "upcoming performance", "Run the full set twice with recovery prompts."
        )

    def technical_focus_month(self, plan: ImprovementPlan) -> ImprovementPlan:
        """Return a copy focused on equipment and sound-check consistency."""
        return self._with_focus(
            plan, "technical focus month", "Practice setup, line check, and monitor requests."
        )

    def maintenance_month(self, plan: ImprovementPlan) -> ImprovementPlan:
        """Return a copy focused on maintaining existing repertoire."""
        return self._with_focus(
            plan, "maintenance month", "Rotate all ready songs through short maintenance sessions."
        )

    def compare(self, left: ImprovementPlan, right: ImprovementPlan) -> tuple[str, ...]:
        """Compare two plans without ranking performers."""
        return (
            f"{left.identifier} focus: {left.focus}",
            f"{right.identifier} focus: {right.focus}",
            f"Shared actions: {len(set(left.actions) & set(right.actions))}",
            "Choose the experiment that best answers the next performance question.",
        )

    def _with_focus(self, plan: ImprovementPlan, focus: str, action: str) -> ImprovementPlan:
        return replace(
            plan,
            identifier=f"{plan.identifier}-{focus.replace(' ', '-')}",
            focus=focus,
            actions=(action, *plan.actions),
            rationale=(f"Experiment added to test {focus}.", *plan.rationale),
            experiment_history=(*plan.experiment_history, focus),
        )
