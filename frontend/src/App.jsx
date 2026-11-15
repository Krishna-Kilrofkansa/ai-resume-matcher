import React, { useState } from 'react';
import {
  Briefcase,
  FileText,
  Upload,
  CheckCircle,
  XCircle,
  Award,
  Layers,
  Search,
  Download,
  X,
  ChevronRight,
  TrendingUp,
  Brain,
  GraduationCap,
  Clock,
  Sparkles
} from 'lucide-react';

const API_BASE = 'http://localhost:8000';

const DEFAULT_SAMPLE_JD = `Title: Senior Backend Engineer (Python / FastAPI)
Company: CloudScale Technologies
Location: Remote (US / Global)
Experience Required: 4+ years of relevant backend software engineering experience
Education: Bachelor's or Master's degree in Computer Science or related technical field

Key Requirements:
- 4+ years of professional backend software development experience.
- Strong proficiency in Python 3 and modern async frameworks (FastAPI or Flask).
- Deep experience with relational databases, specifically PostgreSQL, query optimization, and schema design.
- Hands-on experience with containerization using Docker and orchestration with Kubernetes.
- Practical experience with cloud infrastructure, particularly Amazon Web Services (AWS) or Google Cloud Platform (GCP).
- Proven track record building and securing scalable REST APIs and microservice architectures.
- Solid understanding of Git version control, unit testing (pytest), and CI/CD automation pipelines.

Preferred Skills:
- Experience with Redis caching and asynchronous messaging (RabbitMQ or Kafka).
- Familiarity with frontend frameworks (React or Next.js) for full-stack collaboration.`;

export default function App() {
  const [jdText, setJdText] = useState(DEFAULT_SAMPLE_JD);
  const [jdProfile, setJdProfile] = useState(null);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [extractingJD, setExtractingJD] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [minScoreFilter, setMinScoreFilter] = useState(0);
  const [expandJDSkills, setExpandJDSkills] = useState(false);
  const [expandedSkillsRows, setExpandedSkillsRows] = useState({});

  const toggleRowSkills = (candRank, e) => {
    e.stopPropagation();
    setExpandedSkillsRows((prev) => ({
      ...prev,
      [candRank]: !prev[candRank]
    }));
  };

  // Extract JD Criteria (Module 1)
  const handleExtractJD = async () => {
    if (!jdText.trim()) return;
    setExtractingJD(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/jobs/extract`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jd_text: jdText })
      });
      const data = await res.json();
      setJdProfile(data);
    } catch (err) {
      console.error('Failed to extract JD:', err);
      alert('Could not connect to FastAPI backend. Ensure server is running on port 8000.');
    } finally {
      setExtractingJD(false);
    }
  };

  // Handle Multi-file Selection (Module 2)
  const handleFileChange = (e) => {
    if (e.target.files) {
      setSelectedFiles(Array.from(e.target.files));
    }
  };

  const removeFile = (indexToRemove) => {
    setSelectedFiles((prev) => prev.filter((_, idx) => idx !== indexToRemove));
  };

  const handleLoadSamples = async () => {
    if (!jdText.trim()) {
      alert('Please enter a Job Description first.');
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/resumes/load-samples`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jd_text: jdText })
      });
      const data = await res.json();
      if (res.ok) {
        setRankings(data.rankings || []);
        if (!jdProfile) {
          handleExtractJD();
        }
      } else {
        alert(data.detail || 'Failed to load samples.');
      }
    } catch (err) {
      console.error('Failed to load sample resumes:', err);
      alert('Failed to connect to backend server. Make sure FastAPI is running on http://localhost:8000.');
    } finally {
      setLoading(false);
    }
  };

  // Batch Match and Rank (Module 2 & 3)
  const handleBatchMatch = async () => {
    if (!jdText.trim()) {
      alert('Please enter a Job Description.');
      return;
    }
    if (selectedFiles.length === 0) {
      alert('Please upload at least 1 resume (PDF or DOCX).');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('jd_text', jdText);
    selectedFiles.forEach((file) => {
      formData.append('files', file);
    });

    try {
      const res = await fetch(`${API_BASE}/api/v1/resumes/batch-match`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (res.ok) {
        setRankings(data.rankings || []);
        // Also extract JD profile if not already done
        if (!jdProfile) {
          handleExtractJD();
        }
      } else {
        alert(data.detail || 'Matching failed.');
      }
    } catch (err) {
      console.error('Batch match failed:', err);
      alert('Failed to connect to backend server. Make sure FastAPI is running on http://localhost:8000.');
    } finally {
      setLoading(false);
    }
  };

  // Export ranked candidates to CSV
  const exportToCSV = () => {
    if (!rankings.length) return;
    const headers = ['Rank', 'Candidate Name', 'Overall Score %', 'Relevant Exp (yrs)', 'Matched Skills', 'Missing Skills'];
    const rows = rankings.map((r) => [
      r.rank,
      `"${r.candidate_name}"`,
      r.overall_score,
      r.relevant_experience,
      `"${r.matched_skills.join(', ')}"`,
      `"${r.missing_skills.join(', ')}"`
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'candidate_rankings.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Filter rankings by search query and score slider
  const filteredRankings = rankings.filter((cand) => {
    const matchesSearch =
      cand.candidate_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      cand.matched_skills.some((s) => s.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesScore = cand.overall_score >= minScoreFilter;
    return matchesSearch && matchesScore;
  });

  return (
    <div className="container">
      {/* Header */}
      <header className="header">
        <div>
          <h1>
            <Brain className="text-primary" size={28} color="#2563eb" />
            AI-Based Resume Matching & Ranking System
          </h1>
          <p>
            Precision candidate evaluation powered by <code>bge-small-en-v1.5</code> Chunk MaxSim and a Calibrated 4-Pillar Engine (Optimized for CPU).
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            className="btn-secondary"
            onClick={() => {
              setJdText(DEFAULT_SAMPLE_JD);
              handleExtractJD();
            }}
          >
            <Sparkles size={16} /> Load Senior Python JD
          </button>
        </div>
      </header>

      {/* Top Grid: Module 1 (JD Input) & Module 2 (Batch Upload) */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '24px' }}>
        {/* Module 1: Job Description Input */}
        <div className="card">
          <div className="card-title">
            <Briefcase size={18} color="#2563eb" />
            Module 1: Job Description Input
          </div>
          <textarea
            style={{
              width: '100%',
              height: '180px',
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid #cbd5e1',
              fontSize: '13px',
              fontFamily: 'monospace',
              marginBottom: '12px',
              resize: 'vertical'
            }}
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="Paste raw Job Description here..."
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <button className="btn-secondary" onClick={handleExtractJD} disabled={extractingJD}>
              {extractingJD ? 'Extracting Criteria...' : 'Extract JD Criteria'}
            </button>
            {jdProfile && (
              <span className="badge badge-blue">
                {jdProfile.skills.length} skills identified | {jdProfile.required_years || 'No'} yrs min
              </span>
            )}
          </div>

          {/* Extracted Criteria Preview */}
          {jdProfile && (
            <div style={{ marginTop: '14px', padding: '12px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                <div style={{ fontSize: '12px', fontWeight: '600', color: '#475569' }}>
                  Extracted Criteria ({jdProfile.skills.length} skills):
                </div>
                {jdProfile.skills.length > 10 && (
                  <button
                    type="button"
                    style={{ background: 'transparent', border: 'none', color: '#2563eb', fontSize: '11px', cursor: 'pointer', fontWeight: '600' }}
                    onClick={() => setExpandJDSkills(!expandJDSkills)}
                  >
                    {expandJDSkills ? 'Show less' : 'Expand all'}
                  </button>
                )}
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                {(expandJDSkills ? jdProfile.skills : jdProfile.skills.slice(0, 10)).map((s, idx) => (
                  <span key={idx} className="badge badge-gray">
                    {s}
                  </span>
                ))}
                {!expandJDSkills && jdProfile.skills.length > 10 && (
                  <button
                    type="button"
                    onClick={() => setExpandJDSkills(true)}
                    className="badge badge-blue"
                    style={{ cursor: 'pointer', border: 'none', fontWeight: '600' }}
                    title="Click to expand all extracted skills"
                  >
                    +{jdProfile.skills.length - 10} more
                  </button>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Module 2: Batch Resume Upload */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <div className="card-title" style={{ margin: 0 }}>
              <Upload size={18} color="#2563eb" />
              Module 2: Batch Resume Upload
            </div>
            <button
              className="btn-secondary"
              style={{ fontSize: '12px', padding: '4px 10px' }}
              onClick={handleLoadSamples}
              disabled={loading}
              title="Loads the 12 bundled synthetic test resumes directly from backend"
            >
              <Sparkles size={14} color="#2563eb" /> Load 12 Benchmark Resumes
            </button>
          </div>

          <div
            style={{
              border: '2px dashed #cbd5e1',
              borderRadius: '8px',
              padding: '16px',
              textAlign: 'center',
              backgroundColor: '#f8fafc',
              marginBottom: '12px'
            }}
          >
            <input
              type="file"
              multiple
              accept=".pdf,.docx,.doc"
              id="file-upload"
              style={{ display: 'none' }}
              onChange={handleFileChange}
            />
            <label htmlFor="file-upload" style={{ cursor: 'pointer' }}>
              <FileText size={26} color="#94a3b8" style={{ margin: '0 auto 4px auto' }} />
              <div style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>
                Click to select 10+ resumes or drag & drop
              </div>
              <div style={{ fontSize: '11px', color: '#64748b', marginTop: '2px' }}>
                Supports PDF & DOCX batch upload
              </div>
            </label>
          </div>

          {/* Selected Resumes List Preview */}
          {selectedFiles.length > 0 && (
            <div style={{ marginBottom: '14px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                <span style={{ fontSize: '12px', fontWeight: '600', color: '#475569' }}>
                  Selected Resumes ({selectedFiles.length}):
                </span>
                <button
                  style={{ background: 'transparent', border: 'none', color: '#dc2626', fontSize: '11px', cursor: 'pointer', fontWeight: '500' }}
                  onClick={() => setSelectedFiles([])}
                >
                  Clear all
                </button>
              </div>
              <div
                style={{
                  maxHeight: '135px',
                  overflowY: 'auto',
                  border: '1px solid #e2e8f0',
                  borderRadius: '6px',
                  background: '#ffffff',
                  padding: '6px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px'
                }}
              >
                {selectedFiles.map((file, idx) => {
                  const isPdf = file.name.toLowerCase().endsWith('.pdf');
                  const sizeKb = (file.size / 1024).toFixed(1);
                  return (
                    <div
                      key={idx}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        padding: '4px 8px',
                        background: '#f8fafc',
                        borderRadius: '4px',
                        fontSize: '12px'
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', minWidth: 0, flex: 1 }}>
                        <span className={`badge ${isPdf ? 'badge-red' : 'badge-blue'}`} style={{ fontSize: '10px', padding: '1px 6px' }}>
                          {isPdf ? 'PDF' : 'DOCX'}
                        </span>
                        <span
                          style={{
                            fontWeight: '500',
                            color: '#1e293b',
                            whiteSpace: 'nowrap',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis'
                          }}
                          title={file.name}
                        >
                          {file.name}
                        </span>
                        <span style={{ color: '#94a3b8', fontSize: '11px', flexShrink: 0 }}>
                          ({sizeKb} KB)
                        </span>
                      </div>
                      <button
                        onClick={() => removeFile(idx)}
                        style={{
                          background: 'transparent',
                          border: 'none',
                          color: '#94a3b8',
                          cursor: 'pointer',
                          padding: '2px',
                          display: 'flex',
                          alignItems: 'center'
                        }}
                        title="Remove file"
                      >
                        <X size={14} />
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '12px', color: '#64748b' }}>
              {selectedFiles.length > 0 ? (
                <span>Ready to process <strong>{selectedFiles.length} resume(s)</strong></span>
              ) : (
                'Choose files or load samples'
              )}
            </span>
            <button
              className="btn-primary"
              onClick={handleBatchMatch}
              disabled={loading || selectedFiles.length === 0}
            >
              {loading ? (
                <>Processing {selectedFiles.length} Resumes...</>
              ) : (
                <>
                  <Layers size={16} /> Run AI Matching & Ranking
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Module 4: Candidate Ranking Dashboard */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div className="card-title" style={{ margin: 0 }}>
            <Award size={18} color="#2563eb" />
            Module 4: Candidate Ranking Dashboard
            {rankings.length > 0 && <span className="badge badge-blue">{filteredRankings.length} Candidates</span>}
          </div>

          {/* Dashboard Controls */}
          {rankings.length > 0 && (
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: '#64748b' }}>
                <span>Min Match:</span>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={minScoreFilter}
                  onChange={(e) => setMinScoreFilter(Number(e.target.value))}
                  style={{ width: '100px' }}
                />
                <span style={{ fontWeight: '600', width: '30px' }}>{minScoreFilter}%</span>
              </div>

              <div style={{ position: 'relative' }}>
                <input
                  type="text"
                  placeholder="Filter name or skill..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  style={{
                    padding: '6px 12px 6px 30px',
                    borderRadius: '6px',
                    border: '1px solid #cbd5e1',
                    fontSize: '13px'
                  }}
                />
                <Search size={14} color="#94a3b8" style={{ position: 'absolute', left: '10px', top: '9px' }} />
              </div>

              <button className="btn-secondary" onClick={exportToCSV}>
                <Download size={14} /> Export CSV
              </button>
            </div>
          )}
        </div>

        {/* Candidate Table */}
        {rankings.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px 20px', color: '#64748b' }}>
            <Brain size={40} color="#cbd5e1" style={{ margin: '0 auto 12px auto' }} />
            <p style={{ fontWeight: '500' }}>No candidate evaluations yet.</p>
            <p style={{ fontSize: '13px', marginTop: '4px' }}>
              Upload resumes and click <strong>"Run AI Matching & Ranking"</strong> to generate rankings.
            </p>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table>
              <thead>
                <tr>
                  <th style={{ width: '60px' }}>Rank</th>
                  <th>Candidate</th>
                  <th>Experience</th>
                  <th style={{ width: '180px' }}>Match %</th>
                  <th>Matched Skills</th>
                  <th style={{ width: '100px', textAlign: 'center' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredRankings.map((cand) => {
                  const score = cand.overall_score;
                  let scoreBadgeClass = 'badge-green';
                  let barColor = '#16a34a';
                  if (score < 60) {
                    scoreBadgeClass = 'badge-red';
                    barColor = '#dc2626';
                  } else if (score < 80) {
                    scoreBadgeClass = 'badge-amber';
                    barColor = '#d97706';
                  }

                  return (
                    <tr
                      key={cand.rank}
                      style={{ cursor: 'pointer' }}
                      onClick={() => setSelectedCandidate(cand)}
                    >
                      <td>
                        <span
                          style={{
                            fontWeight: '700',
                            fontSize: '14px',
                            color: cand.rank === 1 ? '#eab308' : cand.rank === 2 ? '#94a3b8' : cand.rank === 3 ? '#b45309' : '#64748b'
                          }}
                        >
                          #{cand.rank}
                        </span>
                      </td>
                      <td>
                        <div style={{ fontWeight: '600', color: '#1e293b' }}>{cand.candidate_name}</div>
                        <div style={{ fontSize: '12px', color: '#64748b' }}>
                          {cand.filename} ({cand.email || 'No email'})
                        </div>
                      </td>
                      <td>
                        <div style={{ fontWeight: '500' }}>{cand.relevant_experience} yrs</div>
                        <div style={{ fontSize: '11px', color: '#64748b' }}>
                          {cand.relevant_experience >= (jdProfile?.required_years || 4.0) ? 'Meets req' : 'Gap in tenure'}
                        </div>
                      </td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <span className={`badge ${scoreBadgeClass}`}>{cand.overall_score}%</span>
                          <div className="progress-bar-bg">
                            <div className="progress-bar-fill" style={{ width: `${cand.overall_score}%`, backgroundColor: barColor }} />
                          </div>
                        </div>
                      </td>
                      <td>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', alignItems: 'center' }}>
                          {(expandedSkillsRows[cand.rank] ? cand.matched_skills : cand.matched_skills.slice(0, 3)).map((s, idx) => (
                            <span key={idx} className="badge badge-green">
                              {s}
                            </span>
                          ))}
                          {cand.matched_skills.length > 3 && (
                            <button
                              type="button"
                              onClick={(e) => toggleRowSkills(cand.rank, e)}
                              className="badge badge-gray"
                              style={{ cursor: 'pointer', border: 'none', fontSize: '11px', fontWeight: '600' }}
                              title={expandedSkillsRows[cand.rank] ? "Collapse skills" : "Click to view all matched skills"}
                            >
                              {expandedSkillsRows[cand.rank] ? "Show less" : `+${cand.matched_skills.length - 3} more`}
                            </button>
                          )}
                        </div>
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        <button
                          className="btn-secondary"
                          style={{ padding: '4px 8px', fontSize: '12px' }}
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedCandidate(cand);
                          }}
                        >
                          Inspect <ChevronRight size={14} />
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Module 5: Candidate-Level Detailed Analysis Drawer */}
      {selectedCandidate && (
        <div className="modal-backdrop" onClick={() => setSelectedCandidate(null)}>
          <div className="drawer" onClick={(e) => e.stopPropagation()}>
            {/* Drawer Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', borderBottom: '1px solid #e2e8f0', paddingBottom: '16px' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="badge badge-blue">Rank #{selectedCandidate.rank}</span>
                  <h2 style={{ fontSize: '20px', fontWeight: '700', color: '#1e293b' }}>
                    {selectedCandidate.candidate_name}
                  </h2>
                </div>
                <div style={{ fontSize: '13px', color: '#64748b', marginTop: '4px' }}>
                  {selectedCandidate.email} | {selectedCandidate.phone || 'No phone'} | File: {selectedCandidate.filename}
                </div>
              </div>
              <button
                style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: '#64748b' }}
                onClick={() => setSelectedCandidate(null)}
              >
                <X size={20} />
              </button>
            </div>

            {/* Overall Score Dial */}
            <div
              style={{
                background: '#f8fafc',
                border: '1px solid #e2e8f0',
                borderRadius: '10px',
                padding: '16px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}
            >
              <div>
                <div style={{ fontSize: '13px', fontWeight: '600', color: '#64748b' }}>Composite Match Score</div>
                <div style={{ fontSize: '32px', fontWeight: '800', color: selectedCandidate.overall_score >= 80 ? '#16a34a' : selectedCandidate.overall_score >= 60 ? '#d97706' : '#dc2626' }}>
                  {selectedCandidate.overall_score}%
                </div>
              </div>
              <div style={{ textAlign: 'right', fontSize: '13px', color: '#475569' }}>
                <div>Relevant Tenure: <strong>{selectedCandidate.relevant_experience} yrs</strong></div>
                <div>Total Experience: <strong>{selectedCandidate.total_experience} yrs</strong></div>
              </div>
            </div>

            {/* 4-Pillar Score Breakdown */}
            <div>
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#1e293b', marginBottom: '10px' }}>
                4-Pillar Calibrated Score Breakdown
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div style={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                    <span>Skills Match (40% wt)</span>
                    <strong>{selectedCandidate.breakdown.skills_score}%</strong>
                  </div>
                  <div className="progress-bar-bg">
                    <div className="progress-bar-fill" style={{ width: `${selectedCandidate.breakdown.skills_score}%`, backgroundColor: '#2563eb' }} />
                  </div>
                </div>

                <div style={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                    <span>Experience Tenure (25% wt)</span>
                    <strong>{selectedCandidate.breakdown.experience_score}%</strong>
                  </div>
                  <div className="progress-bar-bg">
                    <div className="progress-bar-fill" style={{ width: `${selectedCandidate.breakdown.experience_score}%`, backgroundColor: '#16a34a' }} />
                  </div>
                </div>

                <div style={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                    <span>Semantic MaxSim (25% wt)</span>
                    <strong>{selectedCandidate.breakdown.semantic_score}%</strong>
                  </div>
                  <div className="progress-bar-bg">
                    <div className="progress-bar-fill" style={{ width: `${selectedCandidate.breakdown.semantic_score}%`, backgroundColor: '#d97706' }} />
                  </div>
                </div>

                <div style={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                    <span>Education (10% wt)</span>
                    <strong>{selectedCandidate.breakdown.education_score}%</strong>
                  </div>
                  <div className="progress-bar-bg">
                    <div className="progress-bar-fill" style={{ width: `${selectedCandidate.breakdown.education_score}%`, backgroundColor: '#9333ea' }} />
                  </div>
                </div>
              </div>
            </div>

            {/* Skills Matrix: Matched vs Missing */}
            <div>
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#1e293b', marginBottom: '8px' }}>
                Skills Gap Matrix
              </div>
              <div style={{ marginBottom: '10px' }}>
                <div style={{ fontSize: '12px', fontWeight: '600', color: '#16a34a', display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '6px' }}>
                  <CheckCircle size={14} /> Matched Skills ({selectedCandidate.matched_skills.length})
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {selectedCandidate.matched_skills.map((s, idx) => (
                    <span key={idx} className="badge badge-green">
                      {s}
                    </span>
                  ))}
                </div>
              </div>

              {selectedCandidate.missing_skills.length > 0 && (
                <div>
                  <div style={{ fontSize: '12px', fontWeight: '600', color: '#dc2626', display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '6px' }}>
                    <XCircle size={14} /> Missing Required Skills ({selectedCandidate.missing_skills.length})
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {selectedCandidate.missing_skills.map((s, idx) => (
                      <span key={idx} className="badge badge-red">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* AI Explanation & Rationale */}
            <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '16px' }}>
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#1e293b', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Sparkles size={16} color="#2563eb" />
                Score Explanation & Rationale (Module 5)
              </div>
              <ul style={{ paddingLeft: '20px', fontSize: '13px', color: '#334155', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {selectedCandidate.rationale.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>

            {/* Semantic Citations */}
            {selectedCandidate.requirement_citations && selectedCandidate.requirement_citations.length > 0 && (
              <div>
                <div style={{ fontSize: '14px', fontWeight: '600', color: '#1e293b', marginBottom: '8px' }}>
                  Semantic Requirement Citations (Chunk MaxSim)
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {selectedCandidate.requirement_citations.map((cite, idx) => (
                    <div key={idx} style={{ padding: '10px', borderRadius: '6px', border: '1px solid #e2e8f0', background: '#ffffff', fontSize: '12px' }}>
                      <div style={{ fontWeight: '600', color: '#1e293b', marginBottom: '4px' }}>
                        Requirement: "{cite.requirement}"
                      </div>
                      <div style={{ color: '#475569', fontStyle: 'italic', marginBottom: '4px' }}>
                        Matched Evidence: "{cite.best_matching_chunk}"
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748b', fontSize: '11px' }}>
                        <span>Similarity: <strong>{cite.similarity}</strong></span>
                        <span className={`badge ${cite.is_satisfied ? 'badge-green' : 'badge-amber'}`}>
                          {cite.is_satisfied ? 'Requirement Satisfied' : 'Partial Match'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
