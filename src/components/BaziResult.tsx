import React from 'react';

interface BaziResultProps {
    baziData: {
        year: string;
        month: string;
        day: string;
        hour: string;
        elements: string[];
    } | null;
}

const BaziResult: React.FC<BaziResultProps> = ({ baziData }) => {
    if (!baziData) {
        return <div>请先输入出生信息以获取生辰八字。</div>;
    }

    return (
        <div className="bazi-result">
            <h2>您的生辰八字</h2>
            <p>年柱: {baziData.year}</p>
            <p>月柱: {baziData.month}</p>
            <p>日柱: {baziData.day}</p>
            <p>时柱: {baziData.hour}</p>
            <h3>五行信息</h3>
            <ul>
                {baziData.elements.map((element, index) => (
                    <li key={index}>{element}</li>
                ))}
            </ul>
            <style jsx>{`
                .bazi-result {
                    padding: 20px;
                    background-color: #f9f9f9;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }
                h2 {
                    color: #333;
                }
                h3 {
                    color: #666;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    background: #e0f7fa;
                    margin: 5px 0;
                    padding: 10px;
                    border-radius: 5px;
                }
            `}</style>
        </div>
    );
};

export default BaziResult;