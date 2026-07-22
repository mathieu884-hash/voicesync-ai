'use client';

import { PRICING_PLANS } from '@/lib/constants';
import { motion } from 'framer-motion';
import { FaCheck } from 'react-icons/fa';

export default function Pricing() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 p-8">
      <h1 className="text-4xl font-bold text-center mb-4">Simple Pricing</h1>
      <p className="text-center text-slate-400 mb-16">Choose the perfect plan for your needs</p>

      <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-8">
        {PRICING_PLANS.map((plan, i) => (
          <motion.div
            key={plan.id}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className={`card flex flex-col ${
              i === 1 ? 'ring-2 ring-primary md:scale-105' : ''
            }`}
          >
            <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
            <p className="text-4xl font-bold text-primary mb-1">€{plan.price}</p>
            <p className="text-slate-400 mb-6">/month</p>

            <ul className="space-y-3 mb-6 flex-1">
              <li className="flex items-center gap-2">
                <FaCheck className="text-primary" />
                <span>{plan.minutes} minutes/month</span>
              </li>
              <li className="flex items-center gap-2">
                <FaCheck className="text-primary" />
                <span>{plan.languages} languages</span>
              </li>
              <li className="flex items-center gap-2">
                <FaCheck className="text-primary" />
                <span>Up to {plan.quality}</span>
              </li>
              {plan.features.map((feature, j) => (
                <li key={j} className="flex items-center gap-2">
                  <FaCheck className="text-primary" />
                  <span>{feature}</span>
                </li>
              ))}
            </ul>

            <button className="w-full py-2 bg-primary hover:bg-primary/90 text-white rounded-lg font-medium transition">
              Get Started
            </button>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
