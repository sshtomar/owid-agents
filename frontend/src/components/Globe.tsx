import React, { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import createGlobe from "cobe";

export default function Globe() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const pointerRef = useRef<{ x: number; dragging: boolean }>({ x: 0, dragging: false });
  const phiRef = useRef(0);

  useEffect(() => {
    const autoSpeed = 0.003;
    let animationId: number;

    const globe = createGlobe(canvasRef.current!, {
      devicePixelRatio: Math.min(window.devicePixelRatio, 2),
      width: 520 * 2,
      height: 520 * 2,
      phi: 0,
      theta: 0.15,
      dark: 0,
      diffuse: 1.4,
      mapSamples: 16000,
      mapBrightness: 1.2,
      mapBaseBrightness: 0.05,
      baseColor: [0.96, 0.95, 0.91],
      markerColor: [0.92, 0.37, 0.2],
      glowColor: [0.91, 0.9, 0.85],
      markers: [
        { location: [37.78, -122.44], size: 0.03 },
        { location: [51.51, -0.13], size: 0.03 },
        { location: [35.68, 139.65], size: 0.02 },
        { location: [-33.87, 151.21], size: 0.02 },
        { location: [28.61, 77.21], size: 0.03 },
        { location: [-1.29, 36.82], size: 0.02 },
        { location: [55.75, 37.62], size: 0.02 },
        { location: [-23.55, -46.63], size: 0.03 },
        { location: [46.95, 7.45], size: 0.02 },
        { location: [30.04, 31.24], size: 0.02 },
      ],
      opacity: 0.85,
    });

    const canvas = canvasRef.current!;

    function animate() {
      if (!pointerRef.current.dragging) {
        phiRef.current += autoSpeed;
      }
      globe.update({ phi: phiRef.current });
      animationId = requestAnimationFrame(animate);
    }
    animate();

    const onPointerDown = (e: PointerEvent) => {
      pointerRef.current = { x: e.clientX, dragging: true };
      canvas.setPointerCapture(e.pointerId);
    };

    const onPointerMove = (e: PointerEvent) => {
      if (!pointerRef.current.dragging) return;
      const dx = e.clientX - pointerRef.current.x;
      pointerRef.current.x = e.clientX;
      phiRef.current += dx * 0.01;
    };

    const onPointerUp = () => {
      pointerRef.current.dragging = false;
    };

    canvas.addEventListener("pointerdown", onPointerDown);
    canvas.addEventListener("pointermove", onPointerMove);
    canvas.addEventListener("pointerup", onPointerUp);
    canvas.addEventListener("pointerleave", onPointerUp);

    return () => {
      cancelAnimationFrame(animationId);
      canvas.removeEventListener("pointerdown", onPointerDown);
      canvas.removeEventListener("pointermove", onPointerMove);
      canvas.removeEventListener("pointerup", onPointerUp);
      canvas.removeEventListener("pointerleave", onPointerUp);
      globe.destroy();
    };
  }, []);

  return (
    <motion.canvas
      ref={canvasRef}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1.2, delay: 0.3 }}
      style={{
        width: 260,
        height: 260,
        maxWidth: "100%",
        aspectRatio: "1",
        cursor: "grab",
        touchAction: "none",
      }}
    />
  );
}
