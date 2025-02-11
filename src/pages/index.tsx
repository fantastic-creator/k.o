import { useState } from 'react';
import BaziForm from '../components/BaziForm';
import BaziResult from '../components/BaziResult';
import Layout from '../components/Layout';

const Home = () => {
    const [baziResult, setBaziResult] = useState(null);

    const handleBaziCalculation = async (data) => {
        const response = await fetch('/api/calculateBazi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        setBaziResult(result);
    };

    return (
        <Layout>
            <h1>生辰八字计算器</h1>
            <BaziForm onCalculate={handleBaziCalculation} />
            {baziResult && <BaziResult result={baziResult} />}
        </Layout>
    );
};

export default Home;