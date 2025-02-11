import React from 'react';
import Head from 'next/head';
import styles from '../styles/Home.module.css';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <div className={styles.container}>
            <Head>
                <title>生辰八字计算器</title>
                <meta name="description" content="计算您的生辰八字和五行信息" />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <header className={styles.header}>
                <h1>生辰八字计算器</h1>
            </header>
            <main className={styles.main}>
                {children}
            </main>
            <footer className={styles.footer}>
                <p>© 2023 生辰八字计算器. 保留所有权利.</p>
            </footer>
        </div>
    );
};

export default Layout;