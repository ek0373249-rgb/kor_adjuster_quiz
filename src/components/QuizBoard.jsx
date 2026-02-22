import React, { useState, useEffect } from 'react';

function QuizBoard({ questions, finishQuiz, goHome, themeName }) {
    const [currentIdx, setCurrentIdx] = useState(0);
    const [selectedOpt, setSelectedOpt] = useState(null);
    const [showExplanation, setShowExplanation] = useState(false);
    const [answers, setAnswers] = useState([]);
    const [wrongCounts, setWrongCounts] = useState({});

    useEffect(() => {
        const saved = localStorage.getItem('wrong_attempts');
        if (saved) setWrongCounts(JSON.parse(saved));
    }, []);

    const handleSelect = (idx) => {
        if (showExplanation) return;
        setSelectedOpt(idx);
        setShowExplanation(true);

        const q = questions[currentIdx];
        const isCorrect = idx === q.correctAnswer;

        if (!isCorrect) {
            const newCounts = { ...wrongCounts, [q.id]: (wrongCounts[q.id] || 0) + 1 };
            setWrongCounts(newCounts);
            localStorage.setItem('wrong_attempts', JSON.stringify(newCounts));
        }

        setAnswers([...answers, { qId: q.id, selected: idx, isCorrect }]);
    };

    const nextQuestion = () => {
        if (currentIdx < questions.length - 1) {
            setCurrentIdx(currentIdx + 1);
            setSelectedOpt(null);
            setShowExplanation(false);
        } else {
            const finalScore = answers.filter(a => a.isCorrect).length;
            finishQuiz(finalScore, answers);
        }
    };

    const q = questions[currentIdx];
    const progress = ((currentIdx + 1) / questions.length) * 100;

    return (
        <div className="container fade-in" style={{ paddingBottom: '100px' }}>
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <button onClick={goHome} style={{ background: 'transparent', color: 'var(--text-sub)' }}>← 그만하기</button>
                <div style={{ fontSize: '0.9rem', color: 'var(--primary-color)' }}>
                    {themeName === 'mock' ? '랜덤 모의고사' : '집중 학습'} {currentIdx + 1} / {questions.length}
                </div>
            </header>

            <div style={{ height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', marginBottom: '30px' }}>
                <div style={{ width: `${progress}%`, height: '100%', background: 'var(--primary-color)', transition: 'width 0.3s' }}></div>
            </div>

            <div className="glass" style={{ padding: '30px', marginBottom: '20px' }}>
                {wrongCounts[q.id] > 0 && (
                    <div style={{ fontSize: '0.8rem', color: 'var(--wrong)', marginBottom: '10px' }}>
                        ⚠️ 이 문제에서 {wrongCounts[q.id]}번 틀렸습니다
                    </div>
                )}
                <h3 style={{ fontSize: '1.25rem', marginBottom: '20px' }}>{q.question}</h3>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {q.options.map((opt, idx) => {
                        let btnStyle = {
                            padding: '16px',
                            borderRadius: '12px',
                            textAlign: 'left',
                            background: 'rgba(255,255,255,0.05)',
                            fontSize: '1rem',
                            color: 'var(--text-main)', // 글자색 흰색 고정
                            border: '1px solid transparent'
                        };

                        if (showExplanation) {
                            if (idx === q.correctAnswer) btnStyle.border = '2px solid var(--correct)';
                            if (selectedOpt === idx && idx !== q.correctAnswer) btnStyle.border = '2px solid var(--wrong)';
                        }

                        return (
                            <button key={idx} onClick={() => handleSelect(idx)} style={btnStyle} disabled={showExplanation}>
                                {opt}
                            </button>
                        );
                    })}
                </div>
            </div>

            {showExplanation && (
                <div className="fade-in" style={{ marginTop: '30px' }}>
                    <div style={{
                        padding: '24px',
                        borderRadius: '16px',
                        background: selectedOpt === q.correctAnswer ? 'rgba(74, 222, 128, 0.1)' : 'rgba(248, 113, 113, 0.1)',
                        marginBottom: '20px'
                    }}>
                        <h4 style={{ color: selectedOpt === q.correctAnswer ? 'var(--correct)' : 'var(--wrong)', marginBottom: '10px' }}>
                            {selectedOpt === q.correctAnswer ? '🎉 정답입니다!' : '❌ 아쉽네요, 오답입니다.'}
                        </h4>
                        <div style={{ whiteSpace: 'pre-wrap', color: 'var(--text-sub)', fontSize: '0.95rem' }}>
                            {q.explanation}
                        </div>

                        <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
                            <span className="glass" style={{ padding: '4px 10px', fontSize: '0.75rem' }}>#{q.category}</span>
                            <span className="glass" style={{ padding: '4px 10px', fontSize: '0.75rem' }}>#핵심개념</span>
                        </div>
                    </div>

                    <button
                        onClick={nextQuestion}
                        style={{
                            width: '100%',
                            padding: '18px',
                            background: 'var(--primary-color)',
                            color: 'white',
                            fontSize: '1rem',
                            fontWeight: 'bold'
                        }}
                    >
                        {currentIdx < questions.length - 1 ? '다음 문제' : '결과 확인하기'}
                    </button>
                </div>
            )}
        </div>
    );
}

export default QuizBoard;
