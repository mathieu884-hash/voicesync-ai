'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { FaCloudUploadAlt, FaSpinner } from 'react-icons/fa';

export default function DubbingDashboard() {
  const [file, setFile] = useState<File | null>(null);
  const [sourceLanguage, setSourceLanguage] = useState('en');
  const [targetLanguage, setTargetLanguage] = useState('fr');
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = e.target.files?.[0];
    if (uploadedFile) {
      setFile(uploadedFile);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setIsProcessing(true);
    // TODO: Implement actual API call
    for (let i = 0; i <= 100; i += 10) {
      setProgress(i);
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    setIsProcessing(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 p-8">
      <h1 className="text-4xl font-bold text-center mb-12">Dub Your Video</h1>

      <div className="max-w-2xl mx-auto">
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* File Upload */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card border-2 border-dashed border-slate-600 cursor-pointer hover:border-primary transition"
          >
            <label className="flex flex-col items-center justify-center p-12 cursor-pointer">
              <FaCloudUploadAlt className="text-4xl text-primary mb-4" />
              <p className="text-lg font-medium mb-1">
                {file ? file.name : 'Drop your video here'}
              </p>
              <p className="text-slate-400">MP4, MKV, AVI (Max 2GB)</p>
              <input
                type="file"
                className="hidden"
                onChange={handleFileUpload}
                accept="video/*"
              />
            </label>
          </motion.div>

          {/* Language Selection */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="grid md:grid-cols-2 gap-6"
          >
            <div>
              <label className="block text-sm font-medium mb-2">Source Language</label>
              <select
                value={sourceLanguage}
                onChange={(e) => setSourceLanguage(e.target.value)}
                className="input-field"
              >
                <option value="en">English</option>
                <option value="fr">French</option>
                <option value="es">Spanish</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Target Language</label>
              <select
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
                className="input-field"
              >
                <option value="fr">French</option>
                <option value="es">Spanish</option>
                <option value="de">German</option>
              </select>
            </div>
          </motion.div>

          {/* Progress Bar */}
          {isProcessing && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="card"
            >
              <div className="flex items-center gap-4 mb-4">
                <FaSpinner className="animate-spin text-primary" />
                <span className="font-medium">Processing...</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="text-sm text-slate-400 mt-2">{progress}% Complete</p>
            </motion.div>
          )}

          {/* Submit Button */}
          <motion.button
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            type="submit"
            disabled={!file || isProcessing}
            className="w-full py-3 bg-primary hover:bg-primary/90 disabled:opacity-50 text-white font-medium rounded-lg transition"
          >
            {isProcessing ? 'Processing...' : 'Start Dubbing'}
          </motion.button>
        </form>
      </div>
    </div>
  );
}
