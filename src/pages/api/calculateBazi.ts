import type { NextApiRequest, NextApiResponse } from 'next';
import { calculateBazi } from '../../utils/baziCalculator';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'POST') {
        const { year, month, day, hour, minute, gender } = req.body;

        if (!year || !month || !day || !hour || !minute || !gender) {
            return res.status(400).json({ error: '所有字段都是必需的' });
        }

        try {
            const result = calculateBazi(year, month, day, hour, minute, gender);
            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({ error: '计算生辰八字时出错' });
        }
    } else {
        res.setHeader('Allow', ['POST']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}