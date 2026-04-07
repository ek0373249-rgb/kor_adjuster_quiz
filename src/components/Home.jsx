import React, { useState, useEffect } from 'react';

function Home({ startQuiz }) {
    const [counts, setCounts] = useState({ v1: 0, v2: 0, v3: 0 });

    useEffect(() => {
        const saved = localStorage.getItem('wrong_attempts');
        if (saved) {
            const data = JSON.parse(saved);
            const vals = Object.values(data);
            setCounts({
                v1: vals.filter(v => v >= 1).length,
                v2: vals.filter(v => v >= 2).length,
                v3: vals.filter(v => v >= 3).length
            });
        }
    }, []);

    const [activeSubject, setActiveSubject] = useState('재산보험');

    const allThemes = {
        '재산보험': [
            { id: 'fire', name: '화재보험', icon: '🔥', desc: '1~60번 문항' },
            { id: 'inland', name: '동산종합보험', icon: '📦', desc: '61~120번 문항' },
            { id: 'package', name: '패키지보험', icon: '📦', desc: '121~180번 문항' },
            { id: 'bi', name: '기업휴지보험', icon: '⏳', desc: '181~240번 문항' },
            { id: 'reinsurance', name: '재보험', icon: '🤝', desc: '241~300번 문항' },
            { id: 'ox', name: 'OX 특화 문제', icon: '📝', desc: '301~400번 문항' },
        ],
        '배상책임보험': [
            { id: 'liab_gen', name: '일반 영업배상', icon: '🏢', desc: '401~460번 문항' },
            { id: 'liab_prof', name: '전문직업 배상', icon: '👨‍⚕️', desc: '461~520번 문항' },
            { id: 'liab_worker', name: '근로자재해보상', icon: '👷', desc: '521~580번 문항' },
            { id: 'liab_comp', name: '의무 배상책임', icon: '⚖️', desc: '581~640번 문항' },
        ],
        '특종보험': [
            { id: 'spec_eng', name: '기술보험 (Engineering)', icon: '🏗️', desc: '641~700번 문항' },
            { id: 'spec_misc', name: '기타 특종 (동산/도난)', icon: '💎', desc: '701~760번 문항' },
            { id: 'spec_credit', name: '신용 및 보증보험', icon: '💳', desc: '761~820번 문항' },
        ],
        '해상보험': [
            { id: 'marine_cargo', name: '적하보험', icon: '🚢', desc: '821~880번 문항' },
            { id: 'marine_hull', name: '선박보험', icon: '⚓', desc: '881~940번 문항' },
            { id: 'marine_liab', name: '해상 배상책임', icon: '🌊', desc: '941~1000번 문항' },
            { id: 'marine_adj', name: '해상 손해사정', icon: '🔎', desc: '1001~1060번 문항' },
        ]
    };

    const subjects = [
        { title: '재산보험', icon: '🏠' },
        { title: '배상책임보험', icon: '⚖️' },
        { title: '특종보험', icon: '🔧' },
        { title: '해상보험', icon: '⛴️' }
    ];

    return (
        <div className="container fade-in">
            <header style={{ padding: '40px 0', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                <h1 style={{ fontSize: '2rem', marginBottom: '8px' }}>안녕하세요, 수험생님!</h1>
                <p style={{ color: 'var(--text-sub)' }}>오늘도 합격을 향해 한 걸음 더 나아가 볼까요?</p>
            </header>

            <section style={{ marginTop: '40px' }}>
                <h2 style={{ fontSize: '1.2rem', marginBottom: '20px', color: 'var(--primary-color)' }}>과목 대분류 선택 (Subject)</h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '15px' }}>
                    {subjects.map((sub, idx) => (
                        <div
                            key={idx}
                            onClick={() => setActiveSubject(sub.title)}
                            className={`glass ${activeSubject === sub.title ? 'active-tab' : ''}`}
                            style={{ 
                                padding: '20px', 
                                cursor: 'pointer', 
                                transition: 'all 0.3s ease',
                                border: activeSubject === sub.title ? '1px solid var(--primary-color)' : '1px solid rgba(255,255,255,0.1)',
                                textAlign: 'center'
                            }}
                        >
                            <div style={{ fontSize: '1.5rem', marginBottom: '5px' }}>{sub.icon}</div>
                            <h3 style={{ fontSize: '1rem' }}>{sub.title}</h3>
                        </div>
                    ))}
                </div>
            </section>

            <section style={{ marginTop: '40px' }}>
                <h2 style={{ fontSize: '1.2rem', marginBottom: '20px', color: 'var(--primary-color)' }}>나의 학습 도구</h2>
                <div className="glass" style={{ padding: '24px', background: 'rgba(255,255,255,0.02)' }}>
                    <div style={{ marginBottom: '20px' }}>
                        <h3 style={{ marginBottom: '4px' }}>🔴 단계별 오답 공략</h3>
                        <p style={{ fontSize: '0.85rem', color: 'var(--text-sub)' }}>반복적으로 틀리는 문제를 집중적으로 학습하세요.</p>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
                        {[
                            { label: '전체 오답', min: 1, count: counts.v1, color: 'var(--text-main)' },
                            { label: '2회 이상', min: 2, count: counts.v2, color: '#FFD700' },
                            { label: '3회 이상', min: 3, count: counts.v3, color: '#FF4500' }
                        ].map((btn, idx) => (
                            <button
                                key={idx}
                                onClick={() => startQuiz('wrong', btn.min)}
                                style={{
                                    padding: '16px 8px',
                                    background: 'rgba(255,255,255,0.05)',
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center',
                                    gap: '8px'
                                }}
                            >
                                <span style={{ fontSize: '0.75rem', color: 'var(--text-sub)' }}>{btn.label}</span>
                                <span style={{ fontSize: '1.4rem', fontWeight: 'bold', color: btn.color }}>{btn.count}</span>
                            </button>
                        ))}
                    </div>
                </div>
            </section>

            <section style={{ marginTop: '40px' }}>
                <h2 style={{ fontSize: '1.2rem', marginBottom: '20px' }}>{activeSubject} 상세 테마</h2>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                    {allThemes[activeSubject].map(t => (
                        <button
                            key={t.id}
                            className="glass"
                            onClick={() => startQuiz(t.id)}
                            style={{
                                padding: '20px',
                                textAlign: 'left',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '15px',
                                background: 'rgba(255,255,255,0.03)'
                            }}
                        >
                            <span style={{ fontSize: '1.5rem' }}>{t.icon}</span>
                            <div>
                                <div style={{ fontWeight: 'bold' }}>{t.name}</div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-sub)' }}>{t.desc}</div>
                            </div>
                        </button>
                    ))}
                </div>
            </section>

            <div style={{ marginTop: '40px', textAlign: 'center' }}>
                <button
                    onClick={() => startQuiz()}
                    style={{
                        background: 'var(--primary-color)',
                        color: 'white',
                        padding: '18px 40px',
                        fontSize: '1.1rem',
                        fontWeight: 'bold',
                        boxShadow: '0 10px 30px rgba(0, 163, 255, 0.3)'
                    }}
                >
                    랜덤 모의고사 (20문항) 시작하기
                </button>
            </div>
        </div>
    );
}

export default Home;
