import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Template HTML with loading screen and English translation
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mydd - Portfolio</title>
    <style>
        :root {
            /* Dark Theme Variables */
            --bg-primary: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #000000 100%);
            --bg-secondary: rgba(0, 0, 0, 0.6);
            --bg-glass: rgba(0, 0, 0, 0.9);
            --text-primary: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.8);
            --text-tertiary: rgba(255, 255, 255, 0.9);
            --accent-primary: #3b82f6;
            --accent-secondary: #6366f1;
            --accent-tertiary: #8b5cf6;
            --border-color: rgba(59, 130, 246, 0.2);
            --particle-color: rgba(59, 130, 246, 0.1);
            --shadow-color: rgba(0, 0, 0, 0.3);
            --card-bg: rgba(0, 0, 0, 0.6);
            --nav-bg: rgba(0, 0, 0, 0.9);
            --loading-bg: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #000000 100%);
        }

        [data-theme="light"] {
            /* Light Theme Variables */
            --bg-primary: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #ffffff 100%);
            --bg-secondary: rgba(255, 255, 255, 0.8);
            --bg-glass: rgba(255, 255, 255, 0.95);
            --text-primary: #1e293b;
            --text-secondary: rgba(30, 41, 59, 0.8);
            --text-tertiary: rgba(30, 41, 59, 0.9);
            --accent-primary: #0891b2;
            --accent-secondary: #0e7490;
            --accent-tertiary: #155e75;
            --border-color: rgba(8, 145, 178, 0.2);
            --particle-color: rgba(8, 145, 178, 0.1);
            --shadow-color: rgba(0, 0, 0, 0.1);
            --card-bg: rgba(255, 255, 255, 0.8);
            --nav-bg: rgba(255, 255, 255, 0.95);
            --loading-bg: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #ffffff 100%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            overflow-x: hidden;
            height: 100%;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
            scroll-behavior: smooth;
            min-height: 100%;
            position: relative;
            transition: all 0.3s ease;
        }

        /* Theme Toggle Button */
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 2000;
            background: var(--bg-glass);
            backdrop-filter: blur(20px);
            border: 2px solid var(--border-color);
            border-radius: 50px;
            padding: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 8px 32px var(--shadow-color);
            opacity: 0;
            animation: slideDown 1s ease-out 0.8s forwards;
        }

        .theme-toggle:hover {
            transform: translateY(-2px) scale(1.05);
            box-shadow: 0 12px 40px rgba(8, 145, 178, 0.3);
            border-color: var(--accent-primary);
        }

        .theme-toggle-inner {
            position: relative;
            width: 60px;
            height: 30px;
            background: var(--accent-primary);
            border-radius: 25px;
            transition: all 0.3s ease;
        }

        .theme-toggle-slider {
            position: absolute;
            top: 3px;
            left: 3px;
            width: 24px;
            height: 24px;
            background: var(--text-primary);
            border-radius: 50%;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        [data-theme="light"] .theme-toggle-slider {
            transform: translateX(30px);
        }

        .theme-icon {
            width: 16px;
            height: 16px;
            opacity: 1;
            transition: all 0.3s ease;
        }

        .sun-icon {
            opacity: 0;
        }

        [data-theme="light"] .sun-icon {
            opacity: 1;
        }

        [data-theme="light"] .moon-icon {
            opacity: 0;
        }

        /* Loading Screen */
        .loading-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--loading-bg);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            opacity: 1;
            transition: opacity 0.8s ease-out;
        }

        .loading-screen.fade-out {
            opacity: 0;
            pointer-events: none;
        }

        .loading-logo {
            font-size: 4rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 50%, var(--accent-tertiary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }

        .loading-bar {
            width: 200px;
            height: 4px;
            background: var(--border-color);
            border-radius: 2px;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .loading-progress {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            border-radius: 2px;
            width: 0%;
            animation: loadingProgress 2s ease-out forwards;
        }

        .loading-text {
            color: var(--text-secondary);
            font-size: 1.1rem;
            animation: fadeInOut 1.5s infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        @keyframes loadingProgress {
            0% { width: 0%; }
            100% { width: 100%; }
        }

        @keyframes fadeInOut {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }

        .section {
            padding: 100px 0;
            position: relative;
            z-index: 10;
        }

        .contact {
            background: linear-gradient(135deg,
                var(--bg-secondary) 0%,
                rgba(0, 0, 0, 0.3) 30%,
                rgba(10, 10, 10, 0.4) 70%,
                rgba(0, 0, 0, 0.5) 100%
            );
            backdrop-filter: blur(15px);
            position: relative;
            border-top: 1px solid var(--border-color);
            min-height: auto;
            padding-bottom: 50px;
            margin-bottom: 0;
        }

        [data-theme="light"] .contact {
            background: linear-gradient(135deg,
                rgba(255, 255, 255, 0.8) 0%,
                rgba(248, 250, 252, 0.9) 30%,
                rgba(226, 232, 240, 0.95) 70%,
                rgba(241, 245, 249, 1) 100%
            );
        }

        /* Background Animated Particles */
        .bg-particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }

        .particle {
            position: absolute;
            background: var(--particle-color);
            border-radius: 50%;
            animation: floatParticle 15s infinite linear;
        }

        @keyframes floatParticle {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
                opacity: 0;
            }
        }

        /* Navigation */
        nav {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--nav-bg);
            backdrop-filter: blur(20px);
            border-radius: 50px;
            padding: 15px 30px;
            z-index: 1000;
            border: 1px solid var(--border-color);
            box-shadow: 0 8px 32px var(--shadow-color);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            opacity: 0;
            animation: slideDown 1s ease-out 0.5s forwards;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateX(-50%) translateY(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }

        nav:hover {
            transform: translateX(-50%) translateY(-2px);
            box-shadow: 0 12px 40px rgba(8, 145, 178, 0.2);
            border-color: var(--accent-primary);
        }

        nav ul {
            display: flex;
            list-style: none;
            gap: 30px;
            align-items: center;
            margin: 0;
        }

        nav li {
            display: flex;
            align-items: center;
        }

        nav a {
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
            padding: 8px 16px;
            border-radius: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 40px;
            overflow: hidden;
        }

        nav a::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: var(--border-color);
            transition: left 0.3s ease;
            border-radius: 25px;
        }

        nav a:hover::before {
            left: 0;
        }

        nav a:hover {
            transform: scale(1.05);
            color: var(--accent-primary);
        }

        /* Hero Section */
        .hero {
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .hero::before {
            content: '';
            position: absolute;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, var(--particle-color) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: float 20s infinite linear;
        }

        @keyframes float {
            0% { transform: translate(-50px, -50px) rotate(0deg); }
            100% { transform: translate(-50px, -50px) rotate(360deg); }
        }

        .hero-content {
            position: relative;
            z-index: 2;
            max-width: 800px;
            padding: 0 20px;
        }

        .hero h1 {
            font-size: clamp(3rem, 8vw, 8rem);
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 50%, var(--accent-tertiary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
            text-shadow: none;
            opacity: 0;
            animation: titleReveal 2s ease-out 1s forwards;
        }

        @keyframes titleReveal {
            0% {
                opacity: 0;
                transform: scale(0.5) rotateY(90deg);
                filter: blur(20px);
            }
            50% {
                opacity: 0.7;
                transform: scale(1.1) rotateY(45deg);
                filter: blur(5px);
            }
            100% {
                opacity: 1;
                transform: scale(1) rotateY(0deg);
                filter: blur(0px);
            }
        }

        .hero p {
            font-size: clamp(1.2rem, 3vw, 2rem);
            color: var(--text-secondary);
            margin-bottom: 40px;
            opacity: 0;
            animation: typeWriter 3s ease-out 2s forwards;
        }

        @keyframes typeWriter {
            0% {
                opacity: 0;
                width: 0;
            }
            1% {
                opacity: 1;
                width: 0;
            }
            100% {
                opacity: 1;
                width: 100%;
            }
        }

        .cta-button {
            display: inline-block;
            padding: 16px 40px;
            background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary));
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1rem;
            box-shadow: 
                0 10px 30px rgba(8, 145, 178, 0.4),
                0 4px 15px var(--shadow-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            opacity: 0;
            transform: translateY(50px);
            animation: buttonSlideUp 1s ease-out 4s forwards;
        }

        @keyframes buttonSlideUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .cta-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }

        .cta-button:hover::before {
            left: 100%;
        }

        .cta-button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 
                0 15px 40px rgba(8, 145, 178, 0.6),
                0 8px 25px var(--shadow-color);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Advanced Animation Classes */
        .reveal {
            opacity: 0;
            transform: translateY(50px);
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .reveal.active {
            opacity: 1;
            transform: translateY(0);
        }

        .reveal-left {
            opacity: 0;
            transform: translateX(-50px);
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .reveal-left.active {
            opacity: 1;
            transform: translateX(0);
        }

        .reveal-right {
            opacity: 0;
            transform: translateX(50px);
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .reveal-right.active {
            opacity: 1;
            transform: translateX(0);
        }

        .reveal-scale {
            opacity: 0;
            transform: scale(0.8);
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .reveal-scale.active {
            opacity: 1;
            transform: scale(1);
        }

        .reveal-rotate {
            opacity: 0;
            transform: rotateY(90deg);
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .reveal-rotate.active {
            opacity: 1;
            transform: rotateY(0deg);
        }

        /* Staggered animations */
        .stagger-1 { transition-delay: 0.1s; }
        .stagger-2 { transition-delay: 0.2s; }
        .stagger-3 { transition-delay: 0.3s; }
        .stagger-4 { transition-delay: 0.4s; }
        .stagger-5 { transition-delay: 0.5s; }
        .stagger-6 { transition-delay: 0.6s; }

        /* Section Title with Letter Animation */
        .section-title {
            text-align: center;
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 700;
            margin-bottom: 60px;
            background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 50%, var(--accent-tertiary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
        }

        .section-title.letter-reveal .letter {
            display: inline-block;
            opacity: 0;
            transform: translateY(50px) rotateX(-90deg);
            animation: letterDrop 0.6s ease-out forwards;
        }

        @keyframes letterDrop {
            0% {
                opacity: 0;
                transform: translateY(50px) rotateX(-90deg);
            }
            50% {
                opacity: 0.7;
                transform: translateY(-10px) rotateX(-45deg);
            }
            100% {
                opacity: 1;
                transform: translateY(0) rotateX(0deg);
            }
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            width: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            transition: all 0.8s ease;
            transform: translateX(-50%);
        }

        .section-title.active::after {
            width: 100px;
        }

        /* About Section */
        .about {
            background: linear-gradient(135deg, 
                rgba(0, 0, 0, 0.0) 0%,
                rgba(0, 0, 0, 0.2) 25%,
                rgba(0, 0, 0, 0.3) 75%,
                rgba(0, 0, 0, 0.1) 100%
            );
            backdrop-filter: blur(10px);
            position: relative;
            border-top: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
        }

        [data-theme="light"] .about {
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.9) 0%,
                rgba(248, 250, 252, 0.8) 25%,
                rgba(226, 232, 240, 0.7) 75%,
                rgba(241, 245, 249, 0.9) 100%
            );
        }

        .about::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, 
                transparent 49%, 
                var(--particle-color) 50%, 
                transparent 51%
            );
            pointer-events: none;
        }

        /* Skills section */
        .skills {
            background: linear-gradient(135deg,
                rgba(10, 10, 10, 0.1) 0%,
                rgba(26, 26, 26, 0.2) 50%,
                rgba(0, 0, 0, 0.1) 100%
            );
            position: relative;
        }

        [data-theme="light"] .skills {
            background: linear-gradient(135deg,
                rgba(248, 250, 252, 0.9) 0%,
                rgba(226, 232, 240, 0.8) 50%,
                rgba(255, 255, 255, 0.9) 100%
            );
        }

        .about-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }

        .about-text {
            font-size: 1.2rem;
            line-height: 1.8;
            font-weight: 500;
        }

        .about-text p {
            margin-bottom: 20px;
            color: var(--text-tertiary);
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
        }

        .about-text p::before {
            content: '';
            position: absolute;
            left: -20px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(to bottom, var(--accent-primary), transparent);
            opacity: 0;
            transition: opacity 0.6s ease;
        }

        .about-text p.active::before {
            opacity: 1;
        }

        .profile-image {
            width: 300px;
            height: 300px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            box-shadow: 0 20px 60px rgba(8, 145, 178, 0.3);
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
            background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary));
        }

        .profile-image::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(transparent, var(--border-color), transparent);
            animation: rotate 4s linear infinite;
        }

        .profile-image::after {
            content: 'M';
            position: absolute;
            width: 280px;
            height: 280px;
            border-radius: 50%;
            z-index: 2;
            background: var(--bg-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--accent-primary);
            font-size: 4rem;
            font-weight: bold;
        }

        @keyframes rotate {
            100% { transform: rotate(360deg); }
        }

        .profile-image:hover {
            transform: scale(1.05) rotate(3deg);
            box-shadow: 0 25px 80px rgba(8, 145, 178, 0.5);
        }

        /* Skills Section */
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 60px;
        }

        .skill-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 40px 30px;
            text-align: center;
            border: 1px solid var(--border-color);
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 32px var(--shadow-color);
        }

        [data-theme="light"] .skill-card {
            background: rgba(255, 255, 255, 0.9);
        }

        .skill-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, var(--particle-color) 0%, transparent 70%);
            opacity: 0;
            transition: all 0.8s ease;
            transform: scale(0);
        }

        .skill-card.active::before {
            opacity: 1;
            transform: scale(1);
        }

        .skill-card:hover {
            transform: translateY(-10px) rotateY(5deg);
            box-shadow: 
                0 20px 60px rgba(8, 145, 178, 0.3),
                0 10px 30px var(--shadow-color);
            background: linear-gradient(135deg,
                var(--particle-color) 0%,
                var(--border-color) 50%,
                var(--particle-color) 100%
            );
            border-color: var(--accent-primary);
        }

        .project-card:hover {
            transform: translateY(-5px) rotateX(5deg);
            box-shadow: 
                0 25px 80px rgba(8, 145, 178, 0.3),
                0 15px 40px var(--shadow-color);
            border-color: var(--accent-primary);
            background: linear-gradient(135deg,
                var(--particle-color) 0%,
                var(--card-bg) 50%,
                var(--particle-color) 100%
            );
        }

        .skill-icon {
            width: 80px;
            height: 80px;
            background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 2rem;
            box-shadow: 0 10px 30px rgba(8, 145, 178, 0.3);
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            color: white;
            position: relative;
            overflow: hidden;
        }

        .skill-icon::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            transition: all 0.6s ease;
            transform: translate(-50%, -50%);
        }

        .skill-card:hover .skill-icon::before {
            width: 200%;
            height: 200%;
        }

        .skill-card:hover .skill-icon {
            transform: rotate(360deg) scale(1.1);
        }

        .skill-card h3 {
            color: var(--accent-primary);
            font-size: 1.5rem;
            margin-bottom: 15px;
            font-weight: 600;
            background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .skill-card p {
            color: var(--text-tertiary);
            line-height: 1.6;
            font-weight: 500;
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        /* Projects Section */
        .projects {
            background: linear-gradient(135deg,
                rgba(0, 0, 0, 0.1) 0%,
                rgba(0, 0, 0, 0.2) 25%,
                rgba(10, 10, 10, 0.3) 50%,
                rgba(0, 0, 0, 0.2) 75%,
                rgba(0, 0, 0, 0.1) 100%
            );
            position: relative;
            border-top: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
        }

        [data-theme="light"] .projects {
            background: linear-gradient(135deg,
                rgba(255, 255, 255, 0.9) 0%,
                rgba(248, 250, 252, 0.8) 25%,
                rgba(226, 232, 240, 0.7) 50%,
                rgba(241, 245, 249, 0.8) 75%,
                rgba(255, 255, 255, 0.9) 100%
            );
        }

        .projects::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                radial-gradient(circle at 25% 25%, var(--particle-color) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, var(--particle-color) 0%, transparent 50%),
                linear-gradient(45deg, 
                    transparent 49%, 
                    var(--particle-color) 50%, 
                    transparent 51%
                );
            pointer-events: none;
        }

        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 40px;
            margin-top: 60px;
        }

        .project-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            overflow: hidden;
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            border: 1px solid var(--border-color);
            position: relative;
        }

        [data-theme="light"] .project-card {
            background: rgba(255, 255, 255, 0.9);
        }

        .project-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, var(--particle-color), transparent);
            transition: left 0.8s ease;
            z-index: 1;
        }

        .project-card.active::before {
            left: 100%;
        }

        .project-image {
            height: 200px;
            background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary));
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            position: relative;
            overflow: hidden;
            font-size: 3rem;
        }

        .project-image::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }

        .project-card:hover .project-image::before {
            left: 100%;
        }

        .project-content {
            padding: 30px;
            position: relative;
            z-index: 2;
        }

        .project-content h3 {
            color: var(--accent-primary);
            font-size: 1.5rem;
            margin-bottom: 15px;
            font-weight: 600;
            background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .project-content p {
            color: var(--text-tertiary);
            line-height: 1.6;
            margin-bottom: 20px;
            font-weight: 500;
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .project-link {
            display: inline-block;
            color: var(--accent-primary);
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            padding: 8px 20px;
            border: 2px solid var(--accent-primary);
            border-radius: 25px;
            position: relative;
            overflow: hidden;
        }

        .project-link::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: var(--accent-primary);
            transition: left 0.3s ease;
            z-index: -1;
        }

        .project-link:hover::before {
            left: 0;
        }

        .project-link:hover {
            color: white;
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(8, 145, 178, 0.4);
        }

        .contact-content {
            text-align: center;
            max-width: 600px;
            margin: 0 auto;
        }

        .contact-content p {
            font-size: 1.3rem;
            line-height: 1.6;
            font-weight: 500;
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .contact-links {
            display: flex;
            justify-content: center;
            margin-top: 40px;
        }

        .discord-link {
            width: 120px;
            height: 120px;
            background: var(--card-bg);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #5865F2;
            text-decoration: none;
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            border: 3px solid var(--border-color);
            font-size: 3rem;
            position: relative;
            overflow: hidden;
            box-shadow: 
                0 15px 35px rgba(88, 101, 242, 0.2),
                0 8px 20px var(--shadow-color);
        }

        [data-theme="light"] .discord-link {
            background: rgba(255, 255, 255, 0.95);
        }

        .discord-link::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(88, 101, 242, 0.1);
            border-radius: 50%;
            transition: all 0.8s ease;
            transform: translate(-50%, -50%);
        }

        .discord-link::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(transparent, rgba(88, 101, 242, 0.2), transparent);
            animation: rotateDiscord 4s linear infinite;
            opacity: 0;
            transition: opacity 0.5s ease;
        }

        @keyframes rotateDiscord {
            100% { transform: rotate(360deg); }
        }

        .discord-link:hover::before {
            width: 300%;
            height: 300%;
        }

        .discord-link:hover::after {
            opacity: 1;
        }

        .discord-link:hover {
            transform: translateY(-10px) scale(1.15) rotate(-5deg);
            background: rgba(88, 101, 242, 0.1);
            box-shadow: 
                0 25px 60px rgba(88, 101, 242, 0.4),
                0 15px 40px var(--shadow-color);
            border-color: #5865F2;
            color: #5865F2;
        }

        .discord-icon {
            position: relative;
            z-index: 10;
            transition: all 0.3s ease;
        }

        .discord-link:hover .discord-icon {
            transform: scale(1.2) rotate(10deg);
            filter: drop-shadow(0 0 15px rgba(88, 101, 242, 0.6));
        }

        /* Progress Bar */
        .progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), var(--accent-tertiary));
            z-index: 2000;
            transition: width 0.3s ease;
        }

        /* Custom Cursor Trail */
        .cursor-trail {
            position: fixed;
            width: 4px;
            height: 4px;
            background: var(--accent-primary);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9998;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        /* Matrix Rain Effect */
        .matrix-rain {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            opacity: 0.1;
        }

        /* Hologram Effect */
        .hologram {
            position: relative;
            overflow: hidden;
        }

        .hologram::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                var(--particle-color),
                var(--border-color),
                var(--particle-color),
                transparent
            );
            animation: hologramSweep 3s infinite;
        }

        @keyframes hologramSweep {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        /* Neon Glow Effect */
        .neon-glow {
            text-shadow: 
                0 0 5px var(--accent-primary),
                0 0 10px var(--accent-primary),
                0 0 15px var(--accent-primary),
                0 0 20px var(--accent-primary);
            animation: neonFlicker 2s infinite alternate;
        }

        @keyframes neonFlicker {
            0%, 100% {
                text-shadow: 
                    0 0 5px var(--accent-primary),
                    0 0 10px var(--accent-primary),
                    0 0 15px var(--accent-primary),
                    0 0 20px var(--accent-primary);
            }
            50% {
                text-shadow: 
                    0 0 2px var(--accent-primary),
                    0 0 5px var(--accent-primary),
                    0 0 8px var(--accent-primary),
                    0 0 12px var(--accent-primary);
            }
        }

        /* Data Stream Effect */
        .data-stream {
            position: absolute;
            width: 2px;
            height: 40px;
            background: linear-gradient(to bottom, transparent, var(--accent-primary), transparent);
            animation: dataFlow 2s linear infinite;
            opacity: 0.6;
        }

        @keyframes dataFlow {
            0% {
                transform: translateY(-50px);
                opacity: 0;
            }
            50% {
                opacity: 1;
            }
            100% {
                transform: translateY(100vh);
                opacity: 0;
            }
        }

        /* Scroll constraints - FIXED */
        html {
            scroll-behavior: smooth;
            overflow-x: hidden;
            height: 100%;
        }

        body {
            position: relative;
            overflow-x: hidden;
            height: auto;
            max-height: none;
        }

        /* Force exact height calculation */
        .main-content {
            height: auto;
            overflow: hidden;
        }

        .contact {
            margin-bottom: 0 !important;
            padding-bottom: 80px !important;
            position: relative;
        }

        /* Hard stop after contact section */
        .contact::after {
            content: '';
            display: block;
            height: 50px;
            clear: both;
            background: transparent;
        }

        /* Prevent any content after contact */
        .contact ~ * {
            display: none !important;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .theme-toggle {
                top: 15px;
                right: 15px;
            }
            
            .theme-toggle-inner {
                width: 50px;
                height: 25px;
            }
            
            .theme-toggle-slider {
                width: 19px;
                height: 19px;
            }
            
            [data-theme="light"] .theme-toggle-slider {
                transform: translateX(25px);
            }

            nav ul {
                gap: 15px;
            }
            
            nav a {
                padding: 6px 12px;
                font-size: 0.9rem;
            }

            .about-content {
                grid-template-columns: 1fr;
                gap: 40px;
                text-align: center;
            }

            .contact-links {
                justify-content: center;
            }

            .discord-link {
                width: 100px;
                height: 100px;
                font-size: 2.5rem;
            }

            .discord-icon {
                width: 50px;
                height: 50px;
            }

            .loading-logo {
                font-size: 3rem;
            }
        }

        /* Typing Effect */
        .typing-effect {
            overflow: hidden;
            white-space: nowrap;
            border-right: 3px solid var(--accent-primary);
            width: 0;
            animation: typing 3s steps(40, end) forwards, blink 0.8s infinite;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes blink {
            from, to { border-color: transparent }
            50% { border-color: var(--accent-primary) }
        }

        /* Glitch Effect for Titles */
        .glitch {
            position: relative;
        }

        .glitch::before,
        .glitch::after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: inherit;
            opacity: 0;
        }

        .glitch::before {
            animation: glitch1 0.8s infinite;
            color: #ff0000;
            z-index: -1;
        }

        .glitch::after {
            animation: glitch2 0.8s infinite;
            color: #00ff00;
            z-index: -2;
        }

        @keyframes glitch1 {
            0%, 100% {
                transform: translate(0);
                opacity: 0;
            }
            20% {
                transform: translate(-2px, 2px);
                opacity: 0.8;
            }
            40% {
                transform: translate(-2px, -2px);
                opacity: 0.8;
            }
            60% {
                transform: translate(2px, 2px);
                opacity: 0.8;
            }
            80% {
                transform: translate(2px, -2px);
                opacity: 0.8;
            }
        }

        @keyframes glitch2 {
            0%, 100% {
                transform: translate(0);
                opacity: 0;
            }
            20% {
                transform: translate(2px, 2px);
                opacity: 0.6;
            }
            40% {
                transform: translate(2px, -2px);
                opacity: 0.6;
            }
            60% {
                transform: translate(-2px, 2px);
                opacity: 0.6;
            }
            80% {
                transform: translate(-2px, -2px);
                opacity: 0.6;
            }
        }
    </style>
</head>
<body data-theme="dark">
    <!-- Theme Toggle Button -->
    <div class="theme-toggle" id="themeToggle">
        <div class="theme-toggle-inner">
            <div class="theme-toggle-slider">
                <svg class="theme-icon moon-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 3c-4.963 0-9 4.038-9 9s4.037 9 9 9c.424 0 .844-.029 1.258-.087-.74-1.964-.761-4.206-.061-6.223.7-2.017 2.085-3.651 3.894-4.594A6.999 6.999 0 0012 3z"/>
                </svg>
                <svg class="theme-icon sun-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/>
                </svg>
            </div>
        </div>
    </div>

    <!-- Loading Screen -->
    <div class="loading-screen" id="loadingScreen">
        <div class="loading-logo">Mydd</div>
        <div class="loading-bar">
            <div class="loading-progress"></div>
        </div>
        <div class="loading-text">Loading Portfolio...</div>
    </div>

    <!-- Progress Bar -->
    <div class="progress-bar"></div>

    <!-- Matrix Rain Canvas -->
    <canvas class="matrix-rain" id="matrix-canvas"></canvas>

    <!-- Background Particles -->
    <div class="bg-particles" id="particles"></div>

    <!-- Navigation -->
    <nav>
        <ul>
            <li><a href="#home" class="nav-link">Home</a></li>
            <li><a href="#about" class="nav-link">About</a></li>
            <li><a href="#skills" class="nav-link">Skills</a></li>
            <li><a href="#projects" class="nav-link">Projects</a></li>
            <li><a href="#contact" class="nav-link">Contact</a></li>
        </ul>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="hero-content">
            <h1 class="glitch neon-glow" data-text="Mydd">Mydd</h1>
            <p class="typing-effect">Web Developer & Community Manager</p>
            <a href="#about" class="cta-button hologram">Discover My Work</a>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="section about">
        <div class="container">
            <h2 class="section-title reveal" data-text="About Me">About Me</h2>
            <div class="about-content">
                <div class="about-text">
                    <p class="reveal-left stagger-1">Hi! I'm Mydd, a passionate web developer specialized in creating modern and intuitive applications.</p>
                    <p class="reveal-left stagger-2">I also manage Discord communities for YouTubers with over 300K subscribers, where I develop technical solutions to improve user experience.</p>
                    <p class="reveal-left stagger-3">My approach combines technical development and understanding of community needs to create truly useful tools.</p>
                </div>
                <div class="profile-image reveal-scale stagger-2 hologram"></div>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="section skills">
        <div class="container">
            <h2 class="section-title reveal" data-text="My Skills">My Skills</h2>
            <div class="skills-grid">
                <div class="skill-card reveal stagger-1 hologram">
                    <div class="skill-icon">💻</div>
                    <h3>Web Development & Technical Solutions</h3>
                    <p>Creating web applications with JavaScript, HTML/CSS, and modern frameworks for optimal user experiences. Development of custom tools and performance optimization for web applications.</p>
                </div>
                <div class="skill-card reveal stagger-2 hologram">
                    <div class="skill-icon">🤖</div>
                    <h3>AI Integration</h3>
                    <p>Developing tools using artificial intelligence to automate and improve processes. Creating smart applications that enhance productivity and user experience.</p>
                </div>
                <div class="skill-card reveal stagger-3 hologram">
                    <div class="skill-icon">👥</div>
                    <h3>Community Management</h3>
                    <p>Managing Discord servers for content creators with large audiences (300K+ subscribers). Advanced configuration, custom bots, and automated moderation.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="section projects">
        <div class="container">
            <h2 class="section-title reveal" data-text="My Projects">My Projects</h2>
            <div class="projects-grid">
                <div class="project-card reveal-left stagger-1">
                    <div class="project-image">📖</div>
                    <div class="project-content">
                        <h3>Wikipedia Summarizer</h3>
                        <p>Web application using Mistral AI to generate intelligent summaries of Wikipedia articles. Modern interface with theme-based search and automatic summary generation.</p>
                        <a href="https://wiki-summarizer.onrender.com/" target="_blank" class="project-link">View Project</a>
                    </div>
                </div>
                <div class="project-card reveal stagger-2">
                    <div class="project-image">💬</div>
                    <div class="project-content">
                        <h3>Premium Discord Servers</h3>
                        <p>Management and development of Discord servers for YouTubers with over 300K subscribers. Advanced configuration, custom bots, and automated moderation systems.</p>
                        <a href="https://discord.gg/UmvPGDFSXt" target="_blank" class="project-link">Learn More</a>
                    </div>
                </div>
                <div class="project-card reveal-right stagger-3">
                    <div class="project-image">🛠️</div>
                    <div class="project-content">
                        <h3>Custom Tools</h3>
                        <p>Development of custom applications and scripts to automate tasks and improve community management workflows. Tailored solutions for specific needs.</p>
                        <a href="#contact" class="project-link">Contact Me</a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="section contact">
        <div class="container">
            <h2 class="section-title reveal" data-text="Let's Work Together">Let's Work Together</h2>
            <div class="contact-content">
                <p class="reveal stagger-1">
                    Do you have a web project or need help managing your Discord community? Feel free to contact me to discuss your needs.
                </p>
                <div class="contact-links">
                    <a href="https://discord.gg/JyzVnvwV" target="_blank" class="discord-link reveal-scale stagger-1" title="Join my Discord">
                        <svg class="discord-icon" width="60" height="60" viewBox="0 0 71 55" fill="currentColor">
                            <g clip-path="url(#clip0)">
                                <path d="M60.1045 4.8978C55.5792 2.8214 50.7265 1.2916 45.6527 0.41542C45.5603 0.39851 45.468 0.440769 45.4204 0.525289C44.7963 1.6353 44.105 3.0834 43.6209 4.2216C38.1637 3.4046 32.7345 3.4046 27.3892 4.2216C26.905 3.0581 26.1886 1.6353 25.5617 0.525289C25.5141 0.443589 25.4218 0.40133 25.3294 0.41542C20.2584 1.2888 15.4057 2.8186 10.8776 4.8978C10.8384 4.9147 10.8048 4.9429 10.7825 4.9795C1.57795 18.7309 -0.943561 32.1443 0.293408 45.3914C0.299005 45.4562 0.335386 45.5182 0.385761 45.5576C6.45866 50.0174 12.3413 52.7249 18.1147 54.5195C18.2071 54.5477 18.305 54.5139 18.3638 54.4378C19.7295 52.5728 20.9469 50.6063 21.9907 48.5383C22.0523 48.4172 21.9935 48.2735 21.8676 48.2256C19.9366 47.4931 18.0979 46.6 16.3292 45.5858C16.1893 45.5041 16.1781 45.304 16.3068 45.2082C16.679 44.9293 17.0513 44.6391 17.4067 44.3461C17.471 44.2926 17.5606 44.2813 17.6362 44.3151C29.2558 49.6202 41.8354 49.6202 53.3179 44.3151C53.3935 44.2785 53.4831 44.2898 53.5502 44.3433C53.9057 44.6363 54.2779 44.9293 54.6529 45.2082C54.7816 45.304 54.7732 45.5041 54.6333 45.5858C52.8646 46.6197 51.0259 47.4931 49.0921 48.2228C48.9662 48.2707 48.9102 48.4172 48.9718 48.5383C50.038 50.6034 51.2554 52.5699 52.5959 54.435C52.6519 54.5139 52.7526 54.5477 52.845 54.5195C58.6464 52.7249 64.529 50.0174 70.6019 45.5576C70.6551 45.5182 70.6887 45.459 70.6943 45.3942C72.1747 30.0791 68.2147 16.7757 60.1968 4.9823C60.1772 4.9429 60.1437 4.9147 60.1045 4.8978ZM23.7259 37.3253C20.2276 37.3253 17.3451 34.1136 17.3451 30.1693C17.3451 26.225 20.1717 23.0133 23.7259 23.0133C27.308 23.0133 30.1626 26.2532 30.1066 30.1693C30.1066 34.1136 27.28 37.3253 23.7259 37.3253ZM47.3178 37.3253C43.8196 37.3253 40.9371 34.1136 40.9371 30.1693C40.9371 26.225 43.7636 23.0133 47.3178 23.0133C50.9 23.0133 53.7545 26.2532 53.6986 30.1693C53.6986 34.1136 50.9 37.3253 47.3178 37.3253Z" fill="currentColor"/>
                            </g>
                            <defs>
                                <clipPath id="clip0">
                                    <rect width="71" height="55" fill="white"/>
                                </clipPath>
                            </defs>
                        </svg>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <script>
        // Theme Manager
        class ThemeManager {
            constructor() {
                this.currentTheme = localStorage.getItem('theme') || 'dark';
                this.themeToggle = document.getElementById('themeToggle');
                this.init();
            }

            init() {
                this.applyTheme(this.currentTheme);
                this.themeToggle.addEventListener('click', () => this.toggleTheme());
            }

            toggleTheme() {
                this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
                this.applyTheme(this.currentTheme);
                localStorage.setItem('theme', this.currentTheme);
            }

            applyTheme(theme) {
                document.body.setAttribute('data-theme', theme);
                
                // Update matrix canvas color
                const canvas = document.getElementById('matrix-canvas');
                if (canvas && window.matrixCtx) {
                    if (theme === 'light') {
                        window.matrixColor = '#0891b2';
                    } else {
                        window.matrixColor = '#3b82f6';
                    }
                }
            }
        }

        // Loading Screen Manager
        class LoadingManager {
            constructor() {
                this.init();
            }

            init() {
                setTimeout(() => {
                    this.hideLoadingScreen();
                }, 2200);
            }

            hideLoadingScreen() {
                const loadingScreen = document.getElementById('loadingScreen');
                loadingScreen.classList.add('fade-out');
                
                setTimeout(() => {
                    loadingScreen.style.display = 'none';
                    document.body.style.overflow = 'auto';
                    new AdvancedAnimations();
                    new InteractionEffects();
                    new ThemeManager();
                }, 800);
            }
        }

        // Advanced Animation System
        class AdvancedAnimations {
            constructor() {
                this.initObserver();
                this.initLightCursorTrail();
                this.initMatrixRain();
                this.initParticles();
                this.initScrollProgress();
                this.initLetterReveal();
                this.initDataStreams();
                this.setupSmoothScrolling();
                this.initParallaxEffects();
                this.fixScrollBounds();
            }

            fixScrollBounds() {
                // Simple scroll limit approach
                let maxScrollReached = false;
                
                window.addEventListener('scroll', () => {
                    const contactSection = document.querySelector('.contact');
                    if (!contactSection) return;
                    
                    const contactRect = contactSection.getBoundingClientRect();
                    const windowHeight = window.innerHeight;
                    
                    // If contact section bottom is at or above window bottom
                    if (contactRect.bottom <= windowHeight && !maxScrollReached) {
                        maxScrollReached = true;
                        // Disable further scrolling
                        document.body.style.overflow = 'hidden';
                        setTimeout(() => {
                            document.body.style.overflow = 'auto';
                            maxScrollReached = false;
                        }, 100);
                    }
                });

                // Prevent wheel scrolling past contact
                window.addEventListener('wheel', (e) => {
                    const contactSection = document.querySelector('.contact');
                    if (!contactSection) return;
                    
                    const contactRect = contactSection.getBoundingClientRect();
                    const windowHeight = window.innerHeight;
                    
                    if (e.deltaY > 0 && contactRect.bottom <= windowHeight) {
                        e.preventDefault();
                    }
                }, { passive: false });

                // Prevent key navigation past contact
                document.addEventListener('keydown', (e) => {
                    const contactSection = document.querySelector('.contact');
                    if (!contactSection) return;
                    
                    const contactRect = contactSection.getBoundingClientRect();
                    const windowHeight = window.innerHeight;
                    
                    if (contactRect.bottom <= windowHeight) {
                        if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === 'End') {
                            e.preventDefault();
                        }
                    }
                });
            }

            initObserver() {
                const observerOptions = {
                    threshold: 0.1,
                    rootMargin: '0px 0px -50px 0px'
                };

                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('active');
                            
                            if (entry.target.classList.contains('section-title')) {
                                this.animateLetters(entry.target);
                            }
                            
                            if (entry.target.classList.contains('skill-card')) {
                                setTimeout(() => {
                                    entry.target.classList.add('active');
                                }, Math.random() * 200);
                            }
                        }
                    });
                }, observerOptions);

                document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .reveal-rotate, .section-title, .skill-card, .project-card').forEach(el => {
                    observer.observe(el);
                });
            }

            animateLetters(element) {
                const text = element.textContent;
                element.innerHTML = '';
                element.classList.add('letter-reveal');
                
                [...text].forEach((letter, index) => {
                    const span = document.createElement('span');
                    span.textContent = letter === ' ' ? '\u00A0' : letter;
                    span.className = 'letter';
                    span.style.animationDelay = `${index * 0.1}s`;
                    element.appendChild(span);
                });
            }

            initLightCursorTrail() {
                const trails = [];
                
                for (let i = 0; i < 3; i++) {
                    const trail = document.createElement('div');
                    trail.className = 'cursor-trail';
                    document.body.appendChild(trail);
                    trails.push({
                        element: trail,
                        x: 0,
                        y: 0
                    });
                }

                let mouseX = 0, mouseY = 0;

                document.addEventListener('mousemove', (e) => {
                    mouseX = e.clientX;
                    mouseY = e.clientY;
                });

                function animateTrails() {
                    trails.forEach((trail, index) => {
                        trail.x += (mouseX - trail.x) * (0.15 - index * 0.03);
                        trail.y += (mouseY - trail.y) * (0.15 - index * 0.03);
                        
                        trail.element.style.opacity = 0.3 - index * 0.1;
                        trail.element.style.left = trail.x - 2 + 'px';
                        trail.element.style.top = trail.y - 2 + 'px';
                        trail.element.style.transform = `scale(${0.8 - index * 0.2})`;
                    });
                    requestAnimationFrame(animateTrails);
                }
                animateTrails();

                document.addEventListener('mouseleave', () => {
                    trails.forEach(trail => trail.element.style.opacity = '0');
                });

                document.addEventListener('mouseenter', () => {
                    trails.forEach((trail, index) => trail.element.style.opacity = 0.3 - index * 0.1);
                });
            }

            initMatrixRain() {
                const canvas = document.getElementById('matrix-canvas');
                const ctx = canvas.getContext('2d');
                window.matrixCtx = ctx;
                window.matrixColor = '#3b82f6';
                
                const updateCanvasSize = () => {
                    canvas.width = window.innerWidth;
                    canvas.height = window.innerHeight;
                };

                updateCanvasSize();

                const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
                const matrixArray = matrix.split("");

                const fontSize = 10;
                const columns = canvas.width / fontSize;

                const drops = [];
                for (let x = 0; x < columns; x++) {
                    drops[x] = 1;
                }

                function drawMatrix() {
                    ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    ctx.fillStyle = window.matrixColor;
                    ctx.font = fontSize + 'px monospace';

                    for (let i = 0; i < drops.length; i++) {
                        const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
                        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

                        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                            drops[i] = 0;
                        }
                        drops[i]++;
                    }
                }

                const matrixInterval = setInterval(drawMatrix, 100);

                window.addEventListener('resize', () => {
                    updateCanvasSize();
                    clearInterval(matrixInterval);
                    setInterval(drawMatrix, 100);
                });
            }

            initParticles() {
                const particlesContainer = document.getElementById('particles');
                
                for (let i = 0; i < 20; i++) {
                    setTimeout(() => {
                        this.createParticle(particlesContainer);
                    }, i * 300);
                }

                setInterval(() => {
                    if (Math.random() > 0.8) {
                        this.createParticle(particlesContainer);
                    }
                }, 2000);
            }

            createParticle(container) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                
                const size = Math.random() * 6 + 2;
                particle.style.width = size + 'px';
                particle.style.height = size + 'px';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
                particle.style.animationDelay = Math.random() * 2 + 's';
                
                container.appendChild(particle);
                
                setTimeout(() => {
                    if (particle.parentNode) {
                        particle.parentNode.removeChild(particle);
                    }
                }, 20000);
            }

            initScrollProgress() {
                const progressBar = document.querySelector('.progress-bar');
                
                window.addEventListener('scroll', () => {
                    const scrollTop = window.pageYOffset;
                    const documentHeight = document.documentElement.scrollHeight - window.innerHeight;
                    const scrollPercent = (scrollTop / documentHeight) * 100;
                    
                    const clampedPercent = Math.min(Math.max(scrollPercent, 0), 100);
                    progressBar.style.width = clampedPercent + '%';
                });
            }

            initDataStreams() {
                const createDataStream = () => {
                    const stream = document.createElement('div');
                    stream.className = 'data-stream';
                    stream.style.left = Math.random() * 100 + '%';
                    stream.style.animationDuration = (Math.random() * 3 + 2) + 's';
                    document.body.appendChild(stream);
                    
                    setTimeout(() => {
                        if (stream.parentNode) {
                            stream.parentNode.removeChild(stream);
                        }
                    }, 5000);
                };

                setInterval(createDataStream, 2000);
            }

            setupSmoothScrolling() {
                document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
                    anchor.addEventListener('click', function (e) {
                        e.preventDefault();
                        const target = document.querySelector(this.getAttribute('href'));
                        if (target) {
                            target.scrollIntoView({
                                behavior: 'smooth',
                                block: 'start'
                            });
                        }
                    });
                });
            }

            initParallaxEffects() {
                let ticking = false;

                function updateParallax() {
                    const scrolled = window.pageYOffset;
                    const rate = scrolled * -0.5;
                    
                    const hero = document.querySelector('.hero');
                    if (hero) {
                        hero.style.transform = 'translateY(' + rate + 'px)';
                    }

                    const nav = document.querySelector('nav');
                    const currentTheme = document.body.getAttribute('data-theme');
                    
                    if (scrolled > 50) {
                        if (currentTheme === 'light') {
                            nav.style.background = 'rgba(255, 255, 255, 0.98)';
                        } else {
                            nav.style.background = 'rgba(0, 0, 0, 0.95)';
                        }
                        nav.style.backdropFilter = 'blur(25px)';
                    } else {
                        if (currentTheme === 'light') {
                            nav.style.background = 'rgba(255, 255, 255, 0.95)';
                        } else {
                            nav.style.background = 'rgba(0, 0, 0, 0.9)';
                        }
                        nav.style.backdropFilter = 'blur(20px)';
                    }

                    ticking = false;
                }

                function requestTick() {
                    if (!ticking) {
                        requestAnimationFrame(updateParallax);
                        ticking = true;
                    }
                }

                window.addEventListener('scroll', requestTick);
            }

            initLetterReveal() {
                // Called from animateLetters when needed
            }
        }

        // Enhanced Mouse Interactions
        class InteractionEffects {
            constructor() {
                this.initHoverAnimations();
                this.initClickRipples();
            }

            initHoverAnimations() {
                document.querySelectorAll('.cta-button, .project-link').forEach(button => {
                    button.addEventListener('mouseenter', function() {
                        this.style.transform = 'translateY(-5px) scale(1.05)';
                        this.style.filter = 'brightness(1.2)';
                    });
                    
                    button.addEventListener('mouseleave', function() {
                        this.style.transform = 'translateY(0) scale(1)';
                        this.style.filter = 'brightness(1)';
                    });
                });

                document.querySelectorAll('.skill-card').forEach(card => {
                    card.addEventListener('mousemove', function(e) {
                        const rect = this.getBoundingClientRect();
                        const x = e.clientX - rect.left;
                        const y = e.clientY - rect.top;
                        const centerX = rect.width / 2;
                        const centerY = rect.height / 2;
                        const rotateX = (y - centerY) / 10;
                        const rotateY = (centerX - x) / 10;
                        
                        this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
                    });
                    
                    card.addEventListener('mouseleave', function() {
                        this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
                    });
                });
            }

            initClickRipples() {
                document.querySelectorAll('.skill-card, .project-card').forEach(element => {
                    element.addEventListener('click', function(e) {
                        const ripple = document.createElement('div');
                        const rect = this.getBoundingClientRect();
                        const size = Math.max(rect.width, rect.height);
                        const x = e.clientX - rect.left - size / 2;
                        const y = e.clientY - rect.top - size / 2;
                        
                        ripple.style.cssText = `
                            position: absolute;
                            width: ${size}px;
                            height: ${size}px;
                            left: ${x}px;
                            top: ${y}px;
                            background: rgba(8, 145, 178, 0.3);
                            border-radius: 50%;
                            pointer-events: none;
                            animation: clickRipple 0.8s ease-out;
                        `;
                        
                        this.style.position = 'relative';
                        this.appendChild(ripple);
                        
                        setTimeout(() => {
                            if (ripple.parentNode) {
                                ripple.parentNode.removeChild(ripple);
                            }
                        }, 800);
                    });
                });
            }
        }

        // Add CSS animations dynamically
        const dynamicStyles = document.createElement('style');
        dynamicStyles.textContent = `
            @keyframes clickRipple {
                0% {
                    transform: scale(0);
                    opacity: 1;
                }
                100% {
                    transform: scale(2);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(dynamicStyles);

        // Initialize loading screen first, then other animations
        document.addEventListener('DOMContentLoaded', () => {
            // Prevent scrolling during loading
            document.body.style.overflow = 'hidden';
            new LoadingManager();
        });
    </script>
</body>
</html>
"""

# Flask Routes
@app.route('/')
def index():
    """Portfolio homepage"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/status')
def status():
    """Endpoint to check server status"""
    return {'status': 'active', 'message': 'Flask server running'}

@app.route('/api/info')
def api_info():
    """API to retrieve portfolio information"""
    return {
        'name': 'Mydd',
        'title': 'Web Developer & Community Manager',
        'skills': [
            'Web Development & Technical Solutions',
            'AI Integration', 
            'Community Management'
        ],
        'server_info': {
            'port': int(os.environ.get('PORT', 5000)),
            'framework': 'Flask',
            'status': 'running'
        }
    }

if __name__ == '__main__':
    # Configuration pour production sur Render
    PORT = int(os.environ.get('PORT', 5000))
    HOST = '0.0.0.0'  # Nécessaire pour Render
    DEBUG = False  # Mode production
    
    print("🚀 Starting Flask server for production...")
    print(f"📡 Server listening on port: {PORT}")
    print("🌐 Ready for deployment on Render")
    
    try:
        app.run(
            host=HOST, 
            port=PORT, 
            debug=DEBUG
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        
    print("\n✅ Server stopped")
