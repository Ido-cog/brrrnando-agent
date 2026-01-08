from typing import List, Dict
from dataclasses import dataclass
from .models import Trip
from .logic import Phase, PHASE_SEARCH_INTENT
from .integrations.search import search_web, search_videos

@dataclass
class Insight:
    title: str
    content: str
    type: str # 'text' or 'video'
    url: str = ""

class DiscoveryEngine:
    def __init__(self):
        pass

    def discover_insights(self, trip: Trip, phase: Phase) -> List[Insight]:
        """
        Orchestrates web search and video discovery based on the trip's current phase.
        """
        intents = PHASE_SEARCH_INTENT.get(phase, [])
        if not intents:
            return []

        insights = []
        resort = trip.resort_name

        for intent in intents:
            query = f"{resort} {intent}"
            
            # For HYPE_DAILY or ACTIVE, try to find videos
            if phase in [Phase.HYPE_DAILY, Phase.ACTIVE]:
                video_results = search_videos(query, max_results=1, timelimit='m')
                for res in video_results:
                    insights.append(Insight(
                        title=res["title"],
                        content=res["description"],
                        type="video",
                        url=res["content"]
                    ))

            # Always try to find some text insights
            text_results = search_web(query, max_results=2)
            for res in text_results:
                insights.append(Insight(
                    title=res["title"],
                    content=res["body"],
                    type="text",
                    url=res["href"]
                ))

        # Deduplicate and limit
        seen_urls = set()
        unique_insights = []
        for insight in insights:
            if insight.url not in seen_urls:
                unique_insights.append(insight)
                seen_urls.add(insight.url)
        
        return unique_insights[:5] # Limit to top 5 insights for the prompt
