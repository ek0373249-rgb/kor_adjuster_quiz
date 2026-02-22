import React from 'react';

function Result({ score, total, answers, goHome, retryQuiz, retryFailed }) {
    const percentage = Math.round((score / total) * 100);

    return (
        <div className="container fade-in" style={{ textAlign: 'center', padding: '60px 20px' }}>
            <div className="glass" style={{ padding: '40px', marginBottom: '30px' }}>
                <h2 style={{ fontSize: '1.5rem', marginBottom: '10px' }}>학습 완료!</h2>
                <div style={{ fontSize: '4rem', fontWeight: 'bold', color: 'var(--primary-color)', margin: '20px 0' }}>
                    {percentage}%
                </div>
                <p style={{ color: 'var(--text-sub)' }}>
                    전체 {total}문제 중 {score}문제를 맞히셨습니다.
                </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '15px' }}>
                <button
                    onClick={goHome}
                    style={{ width: '100%', padding: '18px', background: 'var(--card-bg)', color: 'white' }}
                >
                    홈으로 돌아가기
                </button>
                {total - score > 0 && (
                    <button
                        onClick={retryFailed}
                        style={{ width: '100%', padding: '18px', background: 'var(--wrong)', color: 'white', fontWeight: 'bold', opacity: 0.9 }}
                    >
                        이번 회차 틀린 문제 다시 풀기
                    </button>
                )}
                <button
                    onClick={retryQuiz}
                    style={{ width: '100%', padding: '18px', background: 'var(--primary-color)', color: 'white', fontWeight: 'bold' }}
                >
                    전체 다시 도전하기
                </button>
            </div>

            <div style={{ marginTop: '40px' }}>
                <h3 style={{ fontSize: '1rem', marginBottom: '15px', textAlign: 'left' }}>학습 성취도 분석</h3>
                <div className="glass" style={{ padding: '20px', textAlign: 'left' }}>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-sub)' }}>
                        맞힌 {score}문제는 개념 숙달이 잘 되어 있습니다. 틀린 {total - score}문제는 '오답노트' 탭에서 다시 복습하실 수 있습니다.
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Result;
