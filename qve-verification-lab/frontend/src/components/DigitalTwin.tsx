import React, { useRef, useEffect } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { PerspectiveCamera, OrbitControls, Text } from '@react-three/drei'
import * as THREE from 'three'

const SpacecraftMesh: React.FC = () => {
  const meshRef = useRef<THREE.Group>(null)

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.001
      meshRef.current.rotation.y += 0.002
    }
  })

  return (
    <group ref={meshRef}>
      {/* Fuselage */}
      <mesh position={[0, 0, 0]}>
        <cylinderGeometry args={[0.3, 0.3, 2, 8]} />
        <meshStandardMaterial color="#333333" />
      </mesh>
      {/* Cockpit */}
      <mesh position={[0, 0.5, 0]}>
        <sphereGeometry args={[0.2, 8, 8]} />
        <meshStandardMaterial color="#00ccff" />
      </mesh>
      {/* Wings */}
      <mesh position={[0.6, 0, 0]}>
        <boxGeometry args={[0.1, 0.2, 1.5]} />
        <meshStandardMaterial color="#555555" />
      </mesh>
      <mesh position={[-0.6, 0, 0]}>
        <boxGeometry args={[0.1, 0.2, 1.5]} />
        <meshStandardMaterial color="#555555" />
      </mesh>
      {/* Label */}
      <Text position={[0, -1.5, 0]} fontSize={0.3} color="#ffffff">
        CONCEPTUAL / SIMULATION
      </Text>
    </group>
  )
}

export const DigitalTwin: React.FC = () => {
  return (
    <div className="digital-twin">
      <h3>3D Digital Twin (CONCEPTUAL / SIMULATION)</h3>
      <Canvas>
        <PerspectiveCamera makeDefault position={[0, 0, 5]} />
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <SpacecraftMesh />
        <OrbitControls />
      </Canvas>
      <p className="warning">⚠️ 3D visualization is NOT propulsion evidence</p>
    </div>
  )
}
