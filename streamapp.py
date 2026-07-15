import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 페이지 설정
st.set_page_config(page_title="이중 진자 시뮬레이터", layout="centered")

st.markdown("# 🌀 이중 진자 카오스 시뮬레이터")
st.write("실시간으로 움직이는 카오스 진자를 관찰하고 궤적 데이터를 다운로드하세요.")

# HTML + CSS + JS 코드를 하나의 문자열로 합침
html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            padding: 10px;
            background-color: #0e1117; /* 스트림릿 기본 어두운 배경색 */
            color: white;
            font-family: sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        canvas {
            background-color: #1a1c23;
            border: 2px solid #3f444e;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        .controls {
            margin-top: 15px;
            display: flex;
            gap: 15px;
        }
        button {
            padding: 10px 20px;
            font-size: 14px;
            cursor: pointer;
            background-color: #ff4b4b; /* 스트림릿 시그니처 레드 */
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
            transition: background 0.2s;
        }
        button:hover {
            background-color: #e03e3e;
        }
        #downloadBtn {
            background-color: #29b5e8;
        }
        #downloadBtn:hover {
            background-color: #1a9bc7;
        }
    </style>
</head>
<body>
    <canvas id="simCanvas" width="700" height="500"></canvas>
    <div class="controls">
        <button id="resetBtn">초기화 및 재실행</button>
        <button id="downloadBtn">궤적 데이터(CSV) 다운로드</button>
    </div>

    <script>
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');

        const g = 1;
        const m1 = 10;
        const m2 = 10;
        const r1 = 120;
        const r2 = 120;

        let a1 = Math.PI / 2;
        let a2 = Math.PI / 2.01;
        let a1_v = 0;
        let a2_v = 0;
        let a1_a = 0;
        let a2_a = 0;

        let cx = canvas.width / 2;
        let cy = 180;

        let path = [];
        let timeStep = 0;

        function calculatePhysics() {
            let num1 = -g * (2 * m1 + m2) * Math.sin(a1);
            let num2 = -m2 * g * Math.sin(a1 - 2 * a2);
            let num3 = -2 * Math.sin(a1 - a2) * m2;
            let num4 = a2_v * a2_v * r2 + a1_v * a1_v * r1 * Math.cos(a1 - a2);
            let den = r1 * (2 * m1 + m2 - m2 * Math.cos(2 * a1 - 2 * a2));
            a1_a = (num1 + num2 + num3 * num4) / den;

            num1 = 2 * Math.sin(a1 - a2);
            num2 = (a1_v * a1_v * r1 * (m1 + m2));
            num3 = g * (m1 + m2) * Math.cos(a1);
            num4 = a2_v * a2_v * r2 * m2 * Math.cos(a1 - a2);
            den = r2 * (2 * m1 + m2 - m2 * Math.cos(2 * a1 - 2 * a2));
            a2_a = (num1 * (num2 + num3 + num4)) / den;

            a1_v += a1_a;
            a2_v += a2_a;
            a1 += a1_v;
            a2 += a2_v;

            a1_v *= 0.999;
            a2_v *= 0.999;
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            calculatePhysics();

            let x1 = cx + r1 * Math.sin(a1);
            let y1 = cy + r1 * Math.cos(a1);
            let x2 = x1 + r2 * Math.sin(a2);
            let y2 = y1 + r2 * Math.cos(a2);

            path.push({ t: timeStep++, x: x2.toFixed(2), y: y2.toFixed(2) });
            if (path.length > 800) {
                path.shift();
            }

            ctx.beginPath();
            for (let i = 0; i < path.length; i++) {
                ctx.lineTo(path[i].x, path[i].y);
            }
            ctx.strokeStyle = "rgba(255, 75, 75, 0.6)";
            ctx.lineWidth = 2;
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = "#f0f2f6";
            ctx.lineWidth = 3;
            ctx.stroke();

            ctx.fillStyle = "#ffffff";
            ctx.beginPath(); ctx.arc(cx, cy, 6, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "#1f77b4";
            ctx.beginPath(); ctx.arc(x1, y1, m1, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "#ff4b4b";
            ctx.beginPath(); ctx.arc(x2, y2, m2, 0, Math.PI * 2); ctx.fill();

            requestAnimationFrame(draw);
        }

        document.getElementById('resetBtn').addEventListener('click', () => {
            a1 = Math.PI / 2;
            a2 = Math.PI / 2.01;
            a1_v = 0; a2_v = 0;
            path = [];
            timeStep = 0;
        });

        document.getElementById('downloadBtn').addEventListener('click', () => {
            let csvContent = "data:text/csv;charset=utf-8,Time,X,Y\\n";
            path.forEach(row => {
                csvContent += `${row.t},${row.x},${row.y}\\n`;
            });
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "chaos_trajectory.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });

        draw();
    </script>
</body>
</html>
"""

# 스트림릿 앱에 HTML 렌더링
components.html(html_content, height=600)
