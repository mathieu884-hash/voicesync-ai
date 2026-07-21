'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Play, Zap, Globe, Shield } from 'react-icons/fa';

export default function Home() {
  return (
    <main className="bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Navigation */}
      <nav className="flex justify-between items-center px-8 py-6 bg-slate-900/80 backdrop-blur">
        <div className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
          🎬 VoiceSync AI
        </div>
        <div className="flex gap-4">
          <Link href="/login" className="px-6 py-2 text-slate-300 hover:text-white transition">
            Login
          </Link>
          <Link href="/signup" className="px-6 py-2 bg-primary hover:bg-primary/90 text-white rounded-lg transition">
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-8 py-24 text-center">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent"
        >
          Dub Your Content in Any Language
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto"
        >
          Professional AI-powered video dubbing and lip-synchronization in 50+ languages with premium voice actors
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="flex justify-center gap-4"
        >
          <Link
            href="/dashboard"
            className="px-8 py-3 bg-primary hover:bg-primary/90 text-white rounded-lg font-medium transition"
          >
            Try Free Demo
          </Link>
          <Link
            href="/pricing"
            className="px-8 py-3 border border-primary text-primary hover:bg-primary/10 rounded-lg font-medium transition"
          >
            View Pricing
          </Link>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="max-w-6xl mx-auto px-8 py-24">
        <h2 className="text-3xl font-bold text-center mb-16">Powerful Features</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {[
            { icon: Play, title: 'Auto Dubbing', desc: 'AI-powered voice generation' },
            { icon: Zap, title: 'Lip Sync', desc: 'Perfect mouth movements' },
            { icon: Globe, title: '50+ Languages', desc: 'Global reach' },
            { icon: Shield, title: 'High Quality', desc: 'Professional results' },
          ].map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              className="card text-center"
            >
              <feature.icon className="text-4xl mx-auto mb-4 text-primary" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-slate-400">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Pricing Preview */}
      <section className="max-w-6xl mx-auto px-8 py-24">
        <h2 className="text-3xl font-bold text-center mb-16">Simple Pricing</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { name: 'Basic', price: '€9.99', minutes: '30 min/month' },
            { name: 'Pro', price: '€29.99', minutes: '150 min/month', featured: true },
            { name: 'Studio', price: '€99.99', minutes: '600 min/month' },
          ].map((plan, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              className={`card ${plan.featured ? 'ring-2 ring-primary' : ''}`}
            >
              <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
              <p className="text-3xl font-bold text-primary mb-2">{plan.price}</p>
              <p className="text-slate-400 mb-4">{plan.minutes}</p>
              <button className="w-full py-2 bg-primary hover:bg-primary/90 rounded-lg transition">
                Get Started
              </button>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-950 border-t border-slate-800 py-12">
        <div className="max-w-6xl mx-auto px-8 text-center text-slate-400">
          <p>&copy; 2024 VoiceSync AI. All rights reserved.</p>
        </div>
      </footer>
    </main>
  );
}
