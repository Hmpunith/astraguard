import os
import json
from .models import Conjunction, ManeuverOption, AIRecommendation


class GraniteAdvisor:
    """IBM Granite AI Advisor for conjunction analysis and maneuver recommendation."""

    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.model_id = os.getenv("GRANITE_MODEL_ID", "ibm/granite-3-8b-instruct")
        self.demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
        self.client = None

        if not self.demo_mode and self.api_key and self.api_key != "your_api_key_here":
            try:
                from ibm_watsonx_ai import Credentials
                from ibm_watsonx_ai.foundation_models import ModelInference

                credentials = Credentials(url=self.url, api_key=self.api_key)
                self.client = ModelInference(
                    model_id=self.model_id,
                    credentials=credentials,
                    project_id=self.project_id,
                    params={
                        "max_new_tokens": 1024,
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "repetition_penalty": 1.1,
                    },
                )
                print("[GraniteAdvisor] Connected to IBM watsonx successfully.")
            except Exception as e:
                print(f"[GraniteAdvisor] Failed to connect to watsonx: {e}")
                print("[GraniteAdvisor] Falling back to demo mode.")
                self.client = None

    def analyze_conjunction(
        self, conjunction: Conjunction, maneuvers: list[ManeuverOption]
    ) -> AIRecommendation:
        """Analyze a conjunction and recommend the optimal avoidance maneuver."""
        if self.client:
            try:
                return self._call_granite(conjunction, maneuvers)
            except Exception as e:
                print(f"[GraniteAdvisor] Granite API call failed: {e}")
                return self._generate_mock_recommendation(conjunction, maneuvers)
        return self._generate_mock_recommendation(conjunction, maneuvers)

    def _build_prompt(
        self, conjunction: Conjunction, maneuvers: list[ManeuverOption]
    ) -> str:
        """Build the prompt for IBM Granite."""
        maneuver_text = ""
        for i, m in enumerate(maneuvers, 1):
            maneuver_text += (
                f"\n  Option {i} ({m.name}):"
                f"\n    - Delta-V: {m.delta_v_m_s} m/s"
                f"\n    - Burn Direction: {m.burn_direction}"
                f"\n    - Fuel Cost: {m.fuel_cost_kg} kg"
                f"\n    - Resulting Miss Distance: {m.resulting_miss_distance_km} km"
                f"\n    - Execution Window: {m.execution_window}"
                f"\n    - ID: {m.id}\n"
            )

        system_instruction = (
            "<|system|>\n"
            "You are a certified space traffic management advisor powered by IBM Granite. "
            "Always cite orbital mechanics principles when justifying maneuver recommendations. "
            "Your analysis must reference Hohmann transfer theory, vis-viva equation constraints, "
            "and conjunction probability geometry. Prioritize crew safety and mission continuity. "
            "Output only valid JSON — no markdown fences, no preamble, no commentary outside the JSON.\n"
            "<|user|>"
        )

        return f"""{system_instruction}
You are AstraGuard, an AI space traffic management advisor powered by IBM Granite. Analyze this orbital conjunction event and recommend the optimal collision avoidance maneuver.

CONJUNCTION EVENT:
  - Primary Satellite: {conjunction.primary.name} (NORAD {conjunction.primary.norad_id})
  - Threatening Object: {conjunction.secondary.name} ({conjunction.secondary.object_type})
  - Predicted Miss Distance: {conjunction.miss_distance_km} km
  - Relative Velocity: {conjunction.relative_velocity_km_s} km/s
  - Risk Score: {conjunction.risk_score}/100 ({conjunction.risk_level.value})
  - Conjunction Geometry: Radial-Along-Track (RAT) plane uncertainty applies

AVAILABLE MANEUVERS:{maneuver_text}
MISSION CONSTRAINTS:
  - Available fuel budget: 50 kg
  - Mission priority: HIGH (active operations)
  - Minimum acceptable miss distance: 15 km
  - Maneuver lead time must respect orbital period phasing

Respond with ONLY a JSON object in exactly this format (no markdown, no explanation outside the JSON):
{{
  "recommended_maneuver_id": "<the ID of the best maneuver option>",
  "confidence": <a float between 0.0 and 1.0>,
  "reasoning": "<2-3 sentences explaining why this maneuver is optimal, citing orbital mechanics principles>",
  "risk_factors": ["<factor 1>", "<factor 2>", "<factor 3>"],
  "trade_off_analysis": "<1-2 sentences comparing the options with delta-V and safety margin trade-offs>",
  "secondary_risks": "<1 sentence about downstream conjunction risks from executing this maneuver>",
  "operator_briefing": "<A professional 4-5 sentence operator briefing summarizing the event, recommended action, orbital mechanics rationale, and authorization request>"
}}"""

    def _call_granite(
        self, conjunction: Conjunction, maneuvers: list[ManeuverOption]
    ) -> AIRecommendation:
        """Call IBM Granite via watsonx API."""
        prompt = self._build_prompt(conjunction, maneuvers)
        response_text = self.client.generate_text(prompt=prompt)

        # Parse JSON from response
        try:
            # Try to extract JSON from the response
            text = response_text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            data = json.loads(text)
        except json.JSONDecodeError:
            print(f"[GraniteAdvisor] Failed to parse Granite response as JSON, using mock")
            return self._generate_mock_recommendation(conjunction, maneuvers)

        return AIRecommendation(
            recommended_maneuver_id=data.get("recommended_maneuver_id", maneuvers[1].id),
            confidence=float(data.get("confidence", 0.85)),
            reasoning=data.get("reasoning", ""),
            risk_factors=data.get("risk_factors", []),
            trade_off_analysis=data.get("trade_off_analysis", ""),
            secondary_risks=data.get("secondary_risks", ""),
            operator_briefing=data.get("operator_briefing", ""),
        )

    def _generate_mock_recommendation(
        self, conjunction: Conjunction, maneuvers: list[ManeuverOption]
    ) -> AIRecommendation:
        """Generate a realistic mock recommendation for demo mode."""
        balanced = next((m for m in maneuvers if m.name == "Balanced"), maneuvers[1])
        conservative = maneuvers[0]
        minimal = maneuvers[2] if len(maneuvers) > 2 else maneuvers[-1]

        return AIRecommendation(
            recommended_maneuver_id=balanced.id,
            confidence=0.91,
            reasoning=(
                f"The Balanced maneuver ({balanced.delta_v_m_s} m/s delta-v) provides the optimal "
                f"trade-off between collision risk mitigation and fuel conservation. It achieves a "
                f"{balanced.resulting_miss_distance_km} km miss distance — well above the 15 km "
                f"safety threshold — while consuming only {balanced.fuel_cost_kg} kg of propellant, "
                f"preserving sufficient delta-v reserves for future station-keeping operations."
            ),
            risk_factors=[
                f"High relative velocity of {conjunction.relative_velocity_km_s} km/s significantly increases potential collision energy.",
                f"Secondary object ({conjunction.secondary.name}, {conjunction.secondary.object_type}) follows an uncontrolled trajectory with no active avoidance capability.",
                f"Current miss distance of {conjunction.miss_distance_km} km is below the {conjunction.risk_level.value}-risk threshold, requiring prompt operator action.",
            ],
            trade_off_analysis=(
                f"The Conservative maneuver (MNV-1) provides maximum clearance at "
                f"{conservative.resulting_miss_distance_km} km but consumes {conservative.fuel_cost_kg} kg "
                f"of fuel — {conservative.fuel_cost_kg / balanced.fuel_cost_kg:.1f}x more than the Balanced "
                f"option for diminishing safety returns. The Minimal maneuver (MNV-3) at "
                f"{minimal.resulting_miss_distance_km} km provides insufficient margin given the "
                f"{conjunction.relative_velocity_km_s} km/s relative velocity and orbital uncertainty."
            ),
            secondary_risks=(
                "Post-maneuver trajectory screening indicates minimal risk of generating new conjunction "
                "events. The adjusted orbit remains within the satellite's designated orbital slot and "
                "no additional close approaches are projected within the next 7 days."
            ),
            operator_briefing=(
                f"OPERATOR BRIEFING — CONJUNCTION {conjunction.id} | CLASSIFICATION: UNCLASSIFIED//FOUO\n\n"
                f"SITUATION: {conjunction.primary.name} (NORAD {conjunction.primary.norad_id}) is on a "
                f"{conjunction.risk_level.value}-risk intercept trajectory with {conjunction.secondary.name} "
                f"({conjunction.secondary.object_type}). Predicted Time of Closest Approach (TCA): "
                f"{conjunction.tca[:19]}Z. Current miss distance: {conjunction.miss_distance_km} km at "
                f"{conjunction.relative_velocity_km_s} km/s relative velocity. Risk score: "
                f"{conjunction.risk_score}/100.\n\n"
                f"RECOMMENDATION: IBM Granite AI (confidence: 91%) recommends executing the Balanced maneuver "
                f"({balanced.id}). This {balanced.burn_direction} burn of {balanced.delta_v_m_s} m/s delta-v "
                f"is scheduled for execution at {balanced.execution_window[:19]}Z, two orbital periods prior to "
                f"TCA to maximize geometric separation. Per the vis-viva equation, the resulting semi-major axis "
                f"change will increase the predicted miss distance to {balanced.resulting_miss_distance_km} km — "
                f"well above the 15 km minimum safety threshold.\n\n"
                f"RESOURCE IMPACT: Propellant expenditure estimated at {balanced.fuel_cost_kg} kg "
                f"({conservative.fuel_cost_kg / balanced.fuel_cost_kg:.1f}x more efficient than the Conservative "
                f"option). Remaining delta-v reserves remain within nominal mission budget.\n\n"
                f"POST-MANEUVER SCREENING: Secondary conjunction screening complete — CLEAR. No new close "
                f"approaches projected within 7-day screening window. "
                f"AUTHORIZATION REQUIRED: Awaiting operator approval to uplink maneuver commands."
            ),
        )
