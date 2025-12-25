"use client";

import {
  LiveKitRoom,
  RoomAudioRenderer,
  StartAudio,
  BarVisualizer,
  useConnectionState,
  useVoiceAssistant,
  useLocalParticipant,
} from "@livekit/components-react";
import { ConnectionState } from "livekit-client";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Activity, Shield, Cpu, Zap, Signal, Mic, ArrowLeft, AlertCircle } from "lucide-react";

export default function Home() {
  const [token, setToken] = useState("");
  const [url, setUrl] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isConnecting, setIsConnecting] = useState(false);

  const onConnect = async () => {
    setError(null);
    setIsConnecting(true);
    try {
      const resp = await fetch("/api/token");
      if (!resp.ok) {
        throw new Error(`Failed to get token: ${resp.status}`);
      }
      const data = await resp.json();
      if (data.error) {
        throw new Error(data.error);
      }
      setToken(data.accessToken);
      setUrl(data.url);
    } catch (e) {
      console.error(e);
      setError(e instanceof Error ? e.message : "Failed to connect. Please try again.");
    } finally {
      setIsConnecting(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#0a0a0a] relative overflow-hidden flex flex-col items-center justify-center">
      {/* CRT Overlays */}
      <div className="scanlines" />
      <div className="crt-overlay" />

      {/* Corner HUD Elements */}
      <div className="hud-corner hud-tl" />
      <div className="hud-corner hud-tr" />
      <div className="hud-corner hud-bl" />
      <div className="hud-corner hud-br" />

      <AnimatePresence mode="wait">
        {!token ? (
          <motion.div
            key="landing"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, filter: "blur(20px)" }}
            className="z-10 text-center space-y-12 max-w-4xl px-4"
          >
            <div className="hologram-bg" />

            <div className="space-y-4 w-full">
              <motion.div
                initial={{ y: 20 }}
                animate={{ y: 0 }}
                transition={{ delay: 0.2 }}
                className="flex items-center justify-center gap-4 mb-8"
              >
                <Cpu className="text-red-500 w-8 h-8" />
                <div className="h-px w-24 bg-red-500/30" />
                <Zap className="text-red-500 w-8 h-8" />
              </motion.div>

              <h1 className="text-5xl sm:text-7xl md:text-8xl lg:text-9xl font-black glitch-text tracking-tighter text-white break-words">
                AGENT<span className="text-red-600">ZERO</span>
              </h1>

              <div className="flex justify-between items-center w-full px-4 max-w-sm mx-auto">
                <span className="hud-label flex items-center gap-2">
                  <Activity className="w-3 h-3" /> NEURAL LINK: READY
                </span>
                <span className="hud-label">V.2.5.RC1</span>
              </div>
            </div>

            <motion.button
              whileHover={{ scale: 1.05, boxShadow: "0 0 50px rgba(255,0,0,0.6)" }}
              whileTap={{ scale: 0.95 }}
              onClick={onConnect}
              disabled={isConnecting}
              className="group relative px-20 py-8 overflow-hidden disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <div className="absolute inset-0 border-2 border-red-600" />
              <div className="absolute inset-0 bg-red-600 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
              <span className="relative z-10 font-orbitron tracking-[0.4em] text-2xl uppercase group-hover:text-black transition-colors duration-300">
                {isConnecting ? "[ CONNECTING... ]" : "[ INITIALIZE ]"}
              </span>
            </motion.button>

            {error && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center gap-3 bg-red-900/30 border border-red-500/50 rounded px-4 py-3 text-red-300"
              >
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
                <span className="text-sm font-rajdhani">{error}</span>
              </motion.div>
            )}

            <div className="pt-12 grid grid-cols-3 gap-8 opacity-40">
              <div className="flex flex-col items-center gap-2">
                <Shield className="w-6 h-6" />
                <span className="text-[10px] font-orbitron">SECURE</span>
              </div>
              <div className="flex flex-col items-center gap-2">
                <Signal className="w-6 h-6" />
                <span className="text-[10px] font-orbitron">UPLINK</span>
              </div>
              <div className="flex flex-col items-center gap-2">
                <Activity className="w-6 h-6" />
                <span className="text-[10px] font-orbitron">SYNAPSE</span>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="interface"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="w-full h-full min-h-screen"
          >
            <LiveKitRoom
              token={token}
              serverUrl={url}
              connect={true}
              audio={true}
              video={false}
              className="flex flex-col items-center justify-between min-h-screen relative w-full p-8 overflow-hidden"
            >
              <div className="hologram-bg" />

              {/* Top Status Bar */}
              <motion.div
                initial={{ y: -50 }}
                animate={{ y: 0 }}
                className="w-full flex justify-center z-10 pt-4"
              >
                <StatusHeader />
              </motion.div>

              {/* Main Reactor Core */}
              <div className="flex-1 flex items-center justify-center w-full relative z-10">
                <motion.div
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="reactor-container"
                >
                  <div className="reactor-ring" />
                  <div className="reactor-ring-dashed" />
                  <div className="reactor-ring-data" />
                  <div className="reactor-core-bg" />

                  <div className="relative z-20">
                    <SimpleVoiceVisualizer />
                  </div>
                </motion.div>
              </div>

              {/* Custom Neural Control Bar */}
              <motion.div
                initial={{ y: 50 }}
                animate={{ y: 0 }}
                className="w-full flex justify-center z-20 pb-12"
              >
                <NeuralControlBar />
              </motion.div>

              <RoomAudioRenderer />
              <StartAudio label="Neural Interface Online" />
            </LiveKitRoom>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}

function NeuralControlBar() {
  const { localParticipant } = useLocalParticipant();
  const [isMuted, setIsMuted] = useState(false);
  const state = useConnectionState();

  useEffect(() => {
    setIsMuted(!localParticipant?.isMicrophoneEnabled);
  }, [localParticipant?.isMicrophoneEnabled]);

  const toggleMic = async () => {
    if (localParticipant) {
      await localParticipant.setMicrophoneEnabled(isMuted);
    }
  };

  const handleDisconnect = () => {
    window.location.reload(); // Simplest way to disconnect and reset state
  };

  return (
    <div className="neural-pill">
      <div className="neural-pill-content">
        <button
          onClick={handleDisconnect}
          className="custom-exit-button group"
          title="Back to Home"
        >
          <ArrowLeft className="w-6 h-6 text-red-500/40 group-hover:text-red-500 transition-colors" />
        </button>

        <button
          onClick={toggleMic}
          className="custom-mic-button group"
          title={isMuted ? "Unmute" : "Mute"}
        >
          <div className={`mic-inner ${!isMuted ? 'active' : ''}`}>
            <Mic className={`w-6 h-6 transition-colors ${!isMuted ? 'text-white' : 'text-red-500/50'}`} />
          </div>
        </button>

        <div className="neural-pill-status">
          <div className="flex justify-between items-center mb-1">
            <span className="text-[8px] font-orbitron text-red-500/50 tracking-widest uppercase truncate">
              {isMuted ? "Audio Suspended" : "Audio Active"}
            </span>
            <span className="text-[8px] font-orbitron text-red-500/50 tracking-widest uppercase hidden sm:block">
              {state === ConnectionState.Connected ? "Secure Link" : "Connecting"}
            </span>
          </div>
          <div className="h-px bg-red-500/10 w-full relative">
            <motion.div
              animate={{
                x: ["0%", "100%", "0%"],
                opacity: isMuted ? 0.2 : 1
              }}
              transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
              className="absolute top-0 left-0 w-16 h-px bg-red-500 shadow-[0_0_10px_#ff0000]"
            />
            {!isMuted && (
              <motion.div
                animate={{ opacity: [0.2, 0.5, 0.2] }}
                transition={{ duration: 1, repeat: Infinity }}
                className="absolute inset-0 bg-red-500/5"
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function StatusHeader() {
  const state = useConnectionState();
  const [statusText, setStatusText] = useState("INITIALIZING");

  useEffect(() => {
    if (state === ConnectionState.Connected) {
      setStatusText("NEURAL LINK ONLINE");
    } else if (state === ConnectionState.Connecting) {
      setStatusText("ESTABLISHING SYNAPSE...");
    } else if (state === ConnectionState.Disconnected) {
      setStatusText("LINK SEVERED");
    }
  }, [state]);

  return (
    <div className="status-badge group">
      <div className={`h-2 w-2 rounded-full ${state === ConnectionState.Connected ? 'bg-green-500 shadow-[0_0_10px_#22c55e]' : 'bg-red-500 animate-pulse'}`} />
      <span className="font-orbitron text-xs text-red-100 tracking-[0.3em] uppercase">{statusText}</span>
      <div className="h-px w-0 group-hover:w-12 bg-red-500/50 transition-all duration-500" />
    </div>
  );
}

function SimpleVoiceVisualizer() {
  const { state, audioTrack } = useVoiceAssistant();
  return (
    <div className="relative">
      <BarVisualizer
        state={state}
        barCount={7}
        trackRef={audioTrack}
        className="h-24 w-48 gap-3 bg-transparent"
      />
      {state === "speaking" && (
        <motion.div
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ repeat: Infinity, duration: 1 }}
          className="absolute -inset-4 border border-red-500/20 rounded-lg pointer-events-none"
        />
      )}
    </div>
  );
}
