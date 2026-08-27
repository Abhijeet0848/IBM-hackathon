"""
Visual Knowledge Radar & Weak-Area Diagnostic Engine
Analyzes student quiz history and active recall drills to map conceptual mastery,
identify knowledge gaps, and recommend adaptive 1-day sprint revisions.
"""

from typing import Dict, List, Any

class KnowledgeRadarEngine:
    @staticmethod
    def analyze_quiz_diagnostics(quiz_eval_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes question-level performance to calculate topic-wise mastery.
        """
        if not quiz_eval_results or "breakdown" not in quiz_eval_results:
            return {
                "topics": {},
                "weakest_topic": None,
                "overall_accuracy": 0.0,
                "strongest_topic": None,
                "needs_remediation": False
            }

        breakdown = quiz_eval_results.get("breakdown", [])
        topic_stats: Dict[str, Dict[str, int]] = {}

        for item in breakdown:
            topic = item.get("category") or item.get("topic") or "General Core Concepts"
            # Clean up topic name
            topic = topic.strip().title()
            if topic not in topic_stats:
                topic_stats[topic] = {"correct": 0, "total": 0}
            
            topic_stats[topic]["total"] += 1
            if item.get("is_correct", False):
                topic_stats[topic]["correct"] += 1

        topic_mastery: Dict[str, Dict[str, Any]] = {}
        for top, data in topic_stats.items():
            pct = round((data["correct"] / data["total"]) * 100, 1) if data["total"] > 0 else 0.0
            if pct >= 80:
                tier = "Mastered"
                color = "#16a34a"
                bg = "#f0fdf4"
                border = "#bbf7d0"
                icon = "👑"
            elif pct >= 60:
                tier = "Proficient"
                color = "#2563eb"
                bg = "#eff6ff"
                border = "#bfdbfe"
                icon = "⚡"
            else:
                tier = "Needs Review"
                color = "#dc2626"
                bg = "#fef2f2"
                border = "#fecaca"
                icon = "⚠️"

            topic_mastery[top] = {
                "correct": data["correct"],
                "total": data["total"],
                "accuracy_pct": pct,
                "tier": tier,
                "color": color,
                "bg": bg,
                "border": border,
                "icon": icon
            }

        # Sort topics by accuracy ascending to identify weakest
        sorted_topics = sorted(topic_mastery.items(), key=lambda x: x[1]["accuracy_pct"])
        weakest = sorted_topics[0][0] if sorted_topics else None
        strongest = sorted_topics[-1][0] if sorted_topics else None
        has_weak = sorted_topics[0][1]["accuracy_pct"] < 75 if sorted_topics else False

        tot_corr = quiz_eval_results.get("correct_count", 0)
        tot_q = quiz_eval_results.get("total_questions", len(breakdown))
        overall_acc = round((tot_corr / tot_q) * 100, 1) if tot_q > 0 else 0.0

        return {
            "topics": topic_mastery,
            "weakest_topic": weakest,
            "strongest_topic": strongest,
            "overall_accuracy": overall_acc,
            "needs_remediation": has_weak
        }

    @staticmethod
    def render_diagnostic_dashboard_html(diagnostics: Dict[str, Any]) -> str:
        """
        Renders a modern visual knowledge radar matrix with topic cards and sprint action.
        """
        topics = diagnostics.get("topics", {})
        weakest = diagnostics.get("weakest_topic")
        needs_rem = diagnostics.get("needs_remediation", False)

        if not topics:
            return ""

        topics_cards_html = ""
        for top_name, info in topics.items():
            topics_cards_html += f"""
            <div style="background: {info['bg']}; border: 1.5px solid {info['border']}; border-radius: 12px; padding: 0.9rem 1rem; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <div style="font-weight: 700; font-size: 0.92rem; color: #0f172a;">
                        {info['icon']} {top_name}
                    </div>
                    <div style="font-size: 0.78rem; font-weight: 800; color: {info['color']}; background: #ffffff; border: 1px solid {info['border']}; border-radius: 20px; padding: 0.15rem 0.55rem; text-transform: uppercase;">
                        {info['tier']} ({info['accuracy_pct']}%)
                    </div>
                </div>
                <div style="width: 100%; height: 6px; background: rgba(0,0,0,0.06); border-radius: 6px; overflow: hidden; margin-top: 4px;">
                    <div style="width: {info['accuracy_pct']}%; height: 100%; background: {info['color']}; border-radius: 6px;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #64748b; font-weight: 600; margin-top: 4px;">
                    <span>Score: {info['correct']}/{info['total']} correct</span>
                    <span>{info['accuracy_pct']}% retention</span>
                </div>
            </div>
            """

        remediation_html = ""
        if needs_rem and weakest:
            remediation_html = f"""
            <div style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border: 1.5px solid #fde68a; border-radius: 12px; padding: 0.9rem 1.15rem; margin-top: 1rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.3rem;">🎯</span>
                    <div>
                        <div style="font-weight: 800; font-size: 0.88rem; color: #92400e;">Adaptive Remediation Alert: Focus on "{weakest}"</div>
                        <div style="font-size: 0.78rem; color: #b45309;">Your quiz diagnostics identified this as your highest-priority review area.</div>
                    </div>
                </div>
            </div>
            """

        return f"""
        <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 18px; padding: 1.35rem 1.5rem; margin: 1.25rem 0; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);">
            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.85rem; margin-bottom: 1.15rem; flex-wrap: wrap; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.4rem;">📊</span>
                    <div>
                        <div style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; color: #0f172a;">Visual Knowledge Radar & Diagnostic Matrix</div>
                        <div style="font-size: 0.8rem; color: #64748b;">Topic-by-topic retention mapping and targeted review recommendations</div>
                    </div>
                </div>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 20px; padding: 0.3rem 0.85rem; font-size: 0.8rem; font-weight: 700; color: #475569;">
                    {len(topics)} Topics Analyzed
                </div>
            </div>
            {topics_cards_html}
            {remediation_html}
        </div>
        """
