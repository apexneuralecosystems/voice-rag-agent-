import { AccessToken } from "livekit-server-sdk";
import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const roomName = req.nextUrl.searchParams.get("roomName") || "voice-assistant-room";
  const participantName = req.nextUrl.searchParams.get("participantName") || "User_" + Math.floor(Math.random() * 1000);

  const apiKey = process.env.LIVEKIT_API_KEY;
  const apiSecret = process.env.LIVEKIT_API_SECRET;

  if (!apiKey || !apiSecret) {
    return NextResponse.json(
      { error: "Server misconfigured" },
      { status: 500 }
    );
  }

  const at = new AccessToken(apiKey, apiSecret, {
    identity: participantName,
    ttl: "10m",
  });

  at.addGrant({ roomJoin: true, room: roomName, canPublish: true, canSubscribe: true });

  return NextResponse.json({
    accessToken: await at.toJwt(),
    url: process.env.LIVEKIT_URL,
  });
}
