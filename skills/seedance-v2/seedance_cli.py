import sys
import os
import argparse
import json

# Add the parent directory to the path so we can import the existing SeedanceAPI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from seedance_api import SeedanceAPI

def main():
    parser = argparse.ArgumentParser(description="Seedance 2.0 CLI Wrapper for OpenClaw Skill")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Text to Video
    t2v = subparsers.add_parser("t2v", help="Generate video from text")
    t2v.add_argument("--prompt", required=True, help="Text prompt")
    t2v.add_argument("--aspect_ratio", default="16:9", help="Aspect ratio (16:9, 9:16, etc.)")
    t2v.add_argument("--duration", type=int, default=5, help="Duration in seconds")
    t2v.add_argument("--quality", default="basic", choices=["basic", "high"], help="Quality level")
    t2v.add_argument("--wait", action="store_true", help="Wait for completion")

    # Image to Video
    i2v = subparsers.add_parser("i2v", help="Generate video from image")
    i2v.add_argument("--prompt", help="Optional text prompt")
    i2v.add_argument("--images", required=True, nargs="+", help="List of image URLs")
    i2v.add_argument("--aspect_ratio", default="16:9", help="Aspect ratio")
    i2v.add_argument("--duration", type=int, default=5, help="Duration in seconds")
    i2v.add_argument("--quality", default="basic", choices=["basic", "high"], help="Quality level")
    i2v.add_argument("--wait", action="store_true", help="Wait for completion")

    # Video Edit
    edit = subparsers.add_parser("edit", help="Edit existing video")
    edit.add_argument("--prompt", required=True, help="Edit prompt")
    edit.add_argument("--videos", required=True, nargs="+", help="List of video URLs")
    edit.add_argument("--images", nargs="*", help="List of image URLs")
    edit.add_argument("--aspect_ratio", default="16:9", help="Aspect ratio")
    edit.add_argument("--quality", default="basic", choices=["basic", "high"], help="Quality level")
    edit.add_argument("--remove_watermark", action="store_true", help="Remove watermark")
    edit.add_argument("--wait", action="store_true", help="Wait for completion")

    # Extend Video
    extend = subparsers.add_parser("extend", help="Extend existing video")
    extend.add_argument("--request_id", required=True, help="Request ID to extend")
    extend.add_argument("--prompt", default="", help="Optional prompt")
    extend.add_argument("--duration", type=int, default=5, help="Duration to extend")
    extend.add_argument("--quality", default="basic", choices=["basic", "high"], help="Quality level")
    extend.add_argument("--wait", action="store_true", help="Wait for completion")

    # Status
    status = subparsers.add_parser("status", help="Get task status")
    status.add_argument("--request_id", required=True, help="Request ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        api = SeedanceAPI()
        
        if args.command == "t2v":
            res = api.text_to_video(args.prompt, args.aspect_ratio, args.duration, args.quality)
        elif args.command == "i2v":
            res = api.image_to_video(args.prompt, args.images, args.aspect_ratio, args.duration, args.quality)
        elif args.command == "edit":
            res = api.video_edit(args.prompt, args.videos, args.images, args.aspect_ratio, args.quality, args.remove_watermark)
        elif args.command == "extend":
            res = api.extend_video(args.request_id, args.prompt, args.duration, args.quality)
        elif args.command == "status":
            res = api.get_result(args.request_id)
            print(json.dumps(res, indent=2))
            return
        
        request_id = res.get("request_id")
        
        if args.wait and request_id:
            print(f"Task submitted: {request_id}. Waiting for completion...")
            result = api.wait_for_completion(request_id)
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(res, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
