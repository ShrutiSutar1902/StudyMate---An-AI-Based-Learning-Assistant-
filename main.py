from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from services.gemini_service import refine_query
from services.youtube_service import fetch_videos, fetch_video_stats
from utils.ranking import rank_videos
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="StudyMate API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/recommend")
async def recommend_videos(topic: str = Query(..., min_length=2, max_length=200)):
    try:
        refined_query = await refine_query(topic)
        logger.info(f"Refined query: {refined_query}")

        videos = await fetch_videos(refined_query)
        if not videos:
            raise HTTPException(status_code=404, detail="No videos found for this topic.")

        video_ids = [v["videoId"] for v in videos]
        stats = await fetch_video_stats(video_ids)

        for video in videos:
            vid_id = video["videoId"]
            video["viewCount"] = stats.get(vid_id, {}).get("viewCount", 0)
            video["likeCount"] = stats.get(vid_id, {}).get("likeCount", 0)

        ranked = rank_videos(videos, refined_query)
        return ranked

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
async def health():
    return {"status": "ok"}
