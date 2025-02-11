import React, { useState } from 'react';

const BaziForm: React.FC<{ onSubmit: (data: any) => void }> = ({ onSubmit }) => {
    const [year, setYear] = useState('');
    const [month, setMonth] = useState('');
    const [day, setDay] = useState('');
    const [hour, setHour] = useState('');
    const [gender, setGender] = useState('male');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit({ year, month, day, hour, gender });
    };

    return (
        <form onSubmit={handleSubmit} className="bazi-form">
            <h2>输入出生信息</h2>
            <div>
                <label>年:</label>
                <input type="number" value={year} onChange={(e) => setYear(e.target.value)} required />
            </div>
            <div>
                <label>月:</label>
                <input type="number" value={month} onChange={(e) => setMonth(e.target.value)} required />
            </div>
            <div>
                <label>日:</label>
                <input type="number" value={day} onChange={(e) => setDay(e.target.value)} required />
            </div>
            <div>
                <label>时:</label>
                <input type="number" value={hour} onChange={(e) => setHour(e.target.value)} required />
            </div>
            <div>
                <label>性别:</label>
                <select value={gender} onChange={(e) => setGender(e.target.value)}>
                    <option value="male">男</option>
                    <option value="female">女</option>
                </select>
            </div>
            <button type="submit">计算生辰八字</button>
        </form>
    );
};

export default BaziForm;