# nextjs-bazi-app/nextjs-bazi-app/README.md

# Next.js Bazi App

这是一个基于 Next.js 的生辰八字计算应用，允许用户输入出生日期（年月日时）和性别，并输出生辰八字的五行信息。该项目旨在提供一个响应式设计，符合中国传统审美。

## 功能

- 用户可以输入出生日期和性别。
- 计算并显示生辰八字的五行信息。
- 响应式设计，适配各种设备。

## 项目结构

```
nextjs-bazi-app
├── public
│   ├── favicon.ico
│   └── index.html
├── src
│   ├── components
│   │   ├── BaziForm.tsx
│   │   ├── BaziResult.tsx
│   │   └── Layout.tsx
│   ├── pages
│   │   ├── api
│   │   │   └── calculateBazi.ts
│   │   ├── _app.tsx
│   │   ├── _document.tsx
│   │   └── index.tsx
│   ├── styles
│   │   ├── globals.css
│   │   └── Home.module.css
│   └── utils
│       └── baziCalculator.ts
├── next.config.js
├── package.json
├── tsconfig.json
└── README.md
```

## 安装与运行

1. 克隆该项目：
   ```
   git clone <repository-url>
   ```

2. 进入项目目录：
   ```
   cd nextjs-bazi-app
   ```

3. 安装依赖：
   ```
   npm install
   ```

4. 运行开发服务器：
   ```
   npm run dev
   ```

5. 打开浏览器访问 [http://localhost:3000](http://localhost:3000)。

## 使用方法

在首页，用户可以输入出生日期（年、月、日、时）和性别，点击提交后，将显示计算出的生辰八字的五行信息。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。

## 许可证

该项目使用 MIT 许可证。