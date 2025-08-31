from flask import Flask, render_template_string
import webbrowser
import threading
import time

app = Flask(__name__)

# Template HTML with updated effects
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
            opacity: 1;
            animation: slideDown 1s ease-out 0.3s;
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

        /* Faulty Terminal Background */
        .faulty-terminal-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            opacity: 0.7;
        }

        .faulty-terminal-container canvas {
            width: 100%;
            height: 100%;
        }

        /* Background Animated Particles */
        .bg-particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 2;
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
            opacity: 1;
            animation: slideDown 1s ease-out 0.2s;
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

        .hero-content {
            position: relative;
            z-index: 10;
            max-width: 800px;
            padding: 0 20px;
        }

        /* Text Trail Container */
        .text-trail-container {
            width: 100%;
            height: 200px;
            position: relative;
            margin-bottom: 30px;
        }

        .text-trail {
            width: 100%;
            height: 100%;
        }

        .text-trail canvas {
            width: 100% !important;
            height: 100% !important;
        }

        .hero p {
            font-size: clamp(1.2rem, 3vw, 2rem);
            color: var(--text-secondary);
            margin-bottom: 40px;
            opacity: 1;
            animation: fadeInUp 1s ease-out 0.5s both;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
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
            opacity: 1;
            animation: fadeInUp 1s ease-out 0.8s both;
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
            gap: 30px;
            margin-top: 40px;
        }

        .contact-link {
            width: 80px;
            height: 80px;
            background: var(--card-bg);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--accent-primary);
            text-decoration: none;
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            border: 2px solid var(--border-color);
            font-size: 1.5rem;
            position: relative;
            overflow: hidden;
        }

        [data-theme="light"] .contact-link {
            background: rgba(255, 255, 255, 0.9);
        }

        .contact-link::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: var(--particle-color);
            border-radius: 50%;
            transition: all 0.6s ease;
            transform: translate(-50%, -50%);
        }

        .contact-link:hover::before {
            width: 200%;
            height: 200%;
        }

        .contact-link:hover {
            transform: translateY(-5px) scale(1.1) rotate(10deg);
            background: var(--border-color);
            box-shadow: 0 15px 40px rgba(8, 145, 178, 0.3);
            border-color: var(--accent-primary);
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
                gap: 20px;
            }

            .contact-link {
                width: 60px;
                height: 60px;
            }

            .text-trail-container {
                height: 150px;
            }
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
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

    <!-- Progress Bar -->
    <div class="progress-bar"></div>

    <!-- Faulty Terminal Background -->
    <div class="faulty-terminal-background" id="faultyTerminal"></div>

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
            <div class="text-trail-container" id="textTrailContainer"></div>
            <p>Web Developer & Community Manager</p>
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
                    <a href="#" class="contact-link reveal-scale stagger-1" title="Discord">💬</a>
                    <a href="mailto:contact@mydd.dev" class="contact-link reveal-scale stagger-2" title="Email">📧</a>
                    <a href="#" class="contact-link reveal-scale stagger-3" title="GitHub">💻</a>
                    <a href="#" class="contact-link reveal-scale stagger-4" title="LinkedIn">💼</a>
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
                
                // Update faulty terminal theme
                if (window.faultyTerminalInstance) {
                    const tintColor = theme === 'light' ? '#0891b2' : '#3b82f6';
                    window.faultyTerminalInstance.updateTint(tintColor);
                }

                // Update text trail theme
                if (window.textTrailInstance) {
                    const textColor = theme === 'light' ? '#0891b2' : '#3b82f6';
                    window.textTrailInstance.updateColor(textColor);
                }
            }
        }

        // Text Trail Implementation (adapted from React)
        class TextTrail {
            constructor(container, options = {}) {
                this.container = container;
                this.options = {
                    text: options.text || "Mydd",
                    fontFamily: options.fontFamily || "Figtree",
                    fontWeight: options.fontWeight || "900",
                    noiseFactor: options.noiseFactor || 1,
                    noiseScale: options.noiseScale || 0.0005,
                    rgbPersistFactor: options.rgbPersistFactor || 0.98,
                    alphaPersistFactor: options.alphaPersistFactor || 0.95,
                    startColor: options.startColor || "#3b82f6",
                    textColor: options.textColor || "#3b82f6",
                    backgroundColor: options.backgroundColor || 0x271e37,
                    supersample: options.supersample || 2,
                    ...options
                };
                
                this.init();
            }

            init() {
                const { w, h } = this.getSize();
                
                this.renderer = new THREE.WebGLRenderer({ antialias: true });
                this.renderer.setClearColor(new THREE.Color(this.options.backgroundColor), 1);
                this.renderer.setPixelRatio(window.devicePixelRatio || 1);
                this.renderer.setSize(w, h);
                this.container.appendChild(this.renderer.domElement);

                this.scene = new THREE.Scene();
                this.fluidScene = new THREE.Scene();
                this.clock = new THREE.Clock();
                
                this.cam = new THREE.OrthographicCamera(-w/2, w/2, h/2, -h/2, 0.1, 10);
                this.cam.position.z = 1;

                this.rt0 = new THREE.WebGLRenderTarget(w, h);
                this.rt1 = this.rt0.clone();

                this.setupShaders();
                this.setupGeometry();
                this.setupText();
                this.setupEventListeners();
                this.animate();
            }

            getSize() {
                return {
                    w: this.container.clientWidth,
                    h: this.container.clientHeight
                };
            }

            setupShaders() {
                const vertexShader = `
                    varying vec2 v_uv;
                    void main(){
                        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                        v_uv = uv;
                    }
                `;

                const persistFragmentShader = `
                    uniform sampler2D sampler;
                    uniform float time;
                    uniform vec2 mousePos;
                    uniform float noiseFactor, noiseScale, rgbPersistFactor, alphaPersistFactor;
                    varying vec2 v_uv;
                    
                    vec3 mod289(vec3 x){return x-floor(x*(1./289.))*289.;}
                    vec4 mod289(vec4 x){return x-floor(x*(1./289.))*289.;}
                    vec4 permute(vec4 x){return mod289(((x*34.)+1.)*x);}
                    float snoise3(vec3 v){
                        const vec2 C=vec2(1./6.,1./3.);
                        const vec4 D=vec4(0.,.5,1.,2.);
                        vec3 i=floor(v+dot(v,C.yyy));
                        vec3 x0=v-i+dot(i,C.xxx);
                        vec3 g=step(x0.yzx,x0.xyz);
                        vec3 l=1.-g;
                        vec3 i1=min(g.xyz,l.zxy);
                        vec3 i2=max(g.xyz,l.zxy);
                        vec3 x1=x0-i1+C.xxx;
                        vec3 x2=x0-i2+C.yyy;
                        vec3 x3=x0-D.yyy;
                        i=mod289(i);
                        vec4 p=permute(permute(permute(i.z+vec4(0.,i1.z,i2.z,1.))+i.y+vec4(0.,i1.y,i2.y,1.))+i.x+vec4(0.,i1.x,i2.x,1.));
                        float n_=1./7.; vec3 ns=n_*D.wyz-D.xzx;
                        vec4 j=p-49.*floor(p*ns.z*ns.z);
                        vec4 x_=floor(j*ns.z);
                        vec4 y_=floor(j-7.*x_);
                        vec4 x=x_*ns.x+ns.yyyy;
                        vec4 y=y_*ns.x+ns.yyyy;
                        vec4 h=1.-abs(x)-abs(y);
                        vec4 b0=vec4(x.xy,y.xy);
                        vec4 b1=vec4(x.zw,y.zw);
                        vec4 s0=floor(b0)*2.+1.;
                        vec4 s1=floor(b1)*2.+1.;
                        vec4 sh=-step(h,vec4(0.));
                        vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy;
                        vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;
                        vec3 p0=vec3(a0.xy,h.x);
                        vec3 p1=vec3(a0.zw,h.y);
                        vec3 p2=vec3(a1.xy,h.z);
                        vec3 p3=vec3(a1.zw,h.w);
                        vec4 norm=inversesqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));
                        p0*=norm.x; p1*=norm.y; p2*=norm.z; p3*=norm.w;
                        vec4 m=max(.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.);
                        m*=m;
                        return 42.*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));
                    }
                    
                    void main(){
                        float a=snoise3(vec3(v_uv*noiseFactor,time*.1))*noiseScale;
                        float b=snoise3(vec3(v_uv*noiseFactor,time*.1+100.))*noiseScale;
                        vec4 t=texture2D(sampler,v_uv+vec2(a,b)+mousePos*.005);
                        gl_FragColor=vec4(t.xyz*rgbPersistFactor,alphaPersistFactor);
                    }
                `;

                const textFragmentShader = `
                    uniform sampler2D sampler;
                    uniform vec3 color;
                    varying vec2 v_uv;
                    void main(){
                        vec4 t=texture2D(sampler,v_uv);
                        float alpha=smoothstep(0.1,0.9,t.a);
                        if(alpha<0.01)discard;
                        gl_FragColor=vec4(color,alpha);
                    }
                `;

                const { w, h } = this.getSize();
                
                this.quadMaterial = new THREE.ShaderMaterial({
                    uniforms: {
                        sampler: { value: null },
                        time: { value: 0 },
                        mousePos: { value: new THREE.Vector2(-1, 1) },
                        noiseFactor: { value: this.options.noiseFactor },
                        noiseScale: { value: this.options.noiseScale },
                        rgbPersistFactor: { value: this.options.rgbPersistFactor },
                        alphaPersistFactor: { value: this.options.alphaPersistFactor },
                    },
                    vertexShader,
                    fragmentShader: persistFragmentShader,
                    transparent: true,
                });

                this.labelMaterial = new THREE.ShaderMaterial({
                    uniforms: {
                        sampler: { value: null },
                        color: { value: this.hexToVec3(this.options.textColor) },
                    },
                    vertexShader,
                    fragmentShader: textFragmentShader,
                    transparent: true,
                });
            }

            setupGeometry() {
                const { w, h } = this.getSize();
                
                this.quad = new THREE.Mesh(
                    new THREE.PlaneGeometry(w, h),
                    this.quadMaterial
                );
                this.fluidScene.add(this.quad);

                this.label = new THREE.Mesh(
                    new THREE.PlaneGeometry(Math.min(w, h), Math.min(w, h)),
                    this.labelMaterial
                );
                this.scene.add(this.label);
            }

            setupText() {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d', { alpha: true, colorSpace: 'srgb' });
                
                const max = Math.min(4096, 2048);
                const pixelRatio = (window.devicePixelRatio || 1) * this.options.supersample;
                const canvasSize = max * pixelRatio;
                
                canvas.width = canvasSize;
                canvas.height = canvasSize;
                canvas.style.width = `${max}px`;
                canvas.style.height = `${max}px`;

                ctx.setTransform(1, 0, 0, 1, 0, 0);
                ctx.scale(pixelRatio, pixelRatio);
                ctx.clearRect(0, 0, max, max);
                ctx.imageSmoothingEnabled = true;
                ctx.imageSmoothingQuality = 'high';
                ctx.shadowColor = 'rgba(255,255,255,0.3)';
                ctx.shadowBlur = 2;
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';

                const refSize = 250;
                ctx.font = `${this.options.fontWeight} ${refSize}px ${this.options.fontFamily}`;
                const width = ctx.measureText(this.options.text).width;
                ctx.font = `${this.options.fontWeight} ${(refSize * max) / width}px ${this.options.fontFamily}`;

                const cx = max / 2, cy = max / 2;
                const offs = [
                    [0, 0], [0.1, 0], [-0.1, 0], [0, 0.1], [0, -0.1],
                    [0.1, 0.1], [-0.1, -0.1], [0.1, -0.1], [-0.1, 0.1]
                ];
                ctx.globalAlpha = 1 / offs.length;
                offs.forEach(([dx, dy]) => ctx.fillText(this.options.text, cx + dx, cy + dy));
                ctx.globalAlpha = 1;

                const texture = new THREE.CanvasTexture(canvas);
                texture.generateMipmaps = true;
                texture.minFilter = THREE.LinearMipmapLinearFilter;
                texture.magFilter = THREE.LinearFilter;
                this.labelMaterial.uniforms.sampler.value = texture;
            }

            setupEventListeners() {
                this.mouse = [0, 0];
                this.target = [0, 0];
                
                this.onMove = (e) => {
                    const r = this.container.getBoundingClientRect();
                    this.target[0] = ((e.clientX - r.left) / r.width) * 2 - 1;
                    this.target[1] = ((r.top + r.height - e.clientY) / r.height) * 2 - 1;
                };
                
                this.container.addEventListener('pointermove', this.onMove);

                this.resizeObserver = new ResizeObserver(() => {
                    const { w, h } = this.getSize();
                    this.renderer.setSize(w, h);
                    this.cam.left = -w / 2;
                    this.cam.right = w / 2;
                    this.cam.top = h / 2;
                    this.cam.bottom = -h / 2;
                    this.cam.updateProjectionMatrix();
                    
                    this.quad.geometry.dispose();
                    this.quad.geometry = new THREE.PlaneGeometry(w, h);
                    this.rt0.setSize(w, h);
                    this.rt1.setSize(w, h);
                    this.label.geometry.dispose();
                    this.label.geometry = new THREE.PlaneGeometry(Math.min(w, h), Math.min(w, h));
                });
                this.resizeObserver.observe(this.container);
            }

            hexToVec3(hex) {
                let h = hex.replace("#", "");
                if (h.length === 3) h = h.split("").map((c) => c + c).join("");
                const n = parseInt(h, 16);
                return new THREE.Vector3(
                    ((n >> 16) & 255) / 255,
                    ((n >> 8) & 255) / 255,
                    (n & 255) / 255
                );
            }

            animate() {
                if (!this.renderer) return;
                
                const dt = this.clock.getDelta();
                const speed = dt * 5;
                this.mouse[0] += (this.target[0] - this.mouse[0]) * speed;
                this.mouse[1] += (this.target[1] - this.mouse[1]) * speed;

                this.quadMaterial.uniforms.mousePos.value.set(this.mouse[0], this.mouse[1]);
                this.quadMaterial.uniforms.sampler.value = this.rt1.texture;
                this.quadMaterial.uniforms.time.value = this.clock.getElapsedTime();

                this.renderer.autoClearColor = false;
                this.renderer.setRenderTarget(this.rt0);
                this.renderer.clearColor();
                this.renderer.render(this.fluidScene, this.cam);
                this.renderer.render(this.scene, this.cam);
                this.renderer.setRenderTarget(null);
                this.renderer.render(this.fluidScene, this.cam);
                this.renderer.render(this.scene, this.cam);
                
                [this.rt0, this.rt1] = [this.rt1, this.rt0];
                
                requestAnimationFrame(() => this.animate());
            }

            updateColor(color) {
                this.labelMaterial.uniforms.color.value = this.hexToVec3(color);
            }

            destroy() {
                if (this.resizeObserver) this.resizeObserver.disconnect();
                this.container.removeEventListener('pointermove', this.onMove);
                if (this.renderer) {
                    this.renderer.dispose();
                    if (this.renderer.domElement.parentNode) {
                        this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
                    }
                }
                this.rt0?.dispose();
                this.rt1?.dispose();
                this.quadMaterial?.dispose();
                this.labelMaterial?.dispose();
                this.quad?.geometry?.dispose();
                this.label?.geometry?.dispose();
            }
        }

        // Faulty Terminal Implementation (adapted from React with OGL)
        class FaultyTerminal {
            constructor(container, options = {}) {
                this.container = container;
                this.options = {
                    scale: options.scale || 1,
                    gridMul: options.gridMul || [2, 1],
                    digitSize: options.digitSize || 1.5,
                    timeScale: options.timeScale || 0.3,
                    scanlineIntensity: options.scanlineIntensity || 0.3,
                    glitchAmount: options.glitchAmount || 1,
                    flickerAmount: options.flickerAmount || 1,
                    noiseAmp: options.noiseAmp || 0,
                    chromaticAberration: options.chromaticAberration || 0,
                    dither: options.dither || 0,
                    curvature: options.curvature || 0.2,
                    tint: options.tint || "#3b82f6",
                    mouseReact: options.mouseReact !== false,
                    mouseStrength: options.mouseStrength || 0.2,
                    brightness: options.brightness || 1,
                    dpr: Math.min(window.devicePixelRatio || 1, 2),
                    ...options
                };
                
                this.init();
            }

            init() {
                // Create canvas manually since we don't have OGL
                this.canvas = document.createElement('canvas');
                this.gl = this.canvas.getContext('webgl') || this.canvas.getContext('experimental-webgl');
                
                if (!this.gl) {
                    console.warn('WebGL not supported, falling back to simple background');
                    this.createFallback();
                    return;
                }

                this.container.appendChild(this.canvas);
                this.setupWebGL();
                this.setupEventListeners();
                this.resize();
                this.animate();
            }

            createFallback() {
                // Simple animated background fallback
                this.container.style.background = `
                    linear-gradient(45deg, ${this.options.tint}22 0%, transparent 50%, ${this.options.tint}11 100%),
                    repeating-linear-gradient(
                        90deg,
                        ${this.options.tint}05 0px,
                        ${this.options.tint}10 2px,
                        transparent 4px,
                        transparent 8px
                    )
                `;
                this.container.style.animation = 'terminalFallback 10s infinite linear';
                
                // Add fallback animation
                if (!document.getElementById('fallback-style')) {
                    const style = document.createElement('style');
                    style.id = 'fallback-style';
                    style.textContent = `
                        @keyframes terminalFallback {
                            0% { background-position: 0% 0%, 0px 0px; }
                            100% { background-position: 100% 100%, 20px 0px; }
                        }
                    `;
                    document.head.appendChild(style);
                }
            }

            setupWebGL() {
                // Simple shader setup for terminal effect
                const vertexShaderSource = `
                    attribute vec2 position;
                    varying vec2 vUv;
                    void main() {
                        vUv = (position + 1.0) * 0.5;
                        gl_Position = vec4(position, 0.0, 1.0);
                    }
                `;

                const fragmentShaderSource = `
                    precision mediump float;
                    varying vec2 vUv;
                    uniform float time;
                    uniform vec2 resolution;
                    uniform vec3 tint;
                    uniform float brightness;
                    
                    float random(vec2 st) {
                        return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
                    }
                    
                    float noise(vec2 st) {
                        vec2 i = floor(st);
                        vec2 f = fract(st);
                        vec2 u = f*f*(3.0-2.0*f);
                        return mix( mix( random( i + vec2(0.0,0.0) ),
                                        random( i + vec2(1.0,0.0) ), u.x),
                                   mix( random( i + vec2(0.0,1.0) ),
                                        random( i + vec2(1.0,1.0) ), u.x), u.y);
                    }
                    
                    void main() {
                        vec2 uv = vUv;
                        vec2 grid = uv * vec2(40.0, 25.0);
                        vec2 gridCell = floor(grid);
                        
                        float cellNoise = random(gridCell + floor(time * 2.0));
                        float intensity = step(0.7, cellNoise) * 0.8;
                        
                        // Scanlines
                        float scanline = sin(uv.y * resolution.y * 2.0) * 0.3 + 0.7;
                        
                        // Flickering
                        float flicker = (sin(time * 10.0) + 1.0) * 0.5 * 0.1 + 0.9;
                        
                        vec3 color = tint * intensity * scanline * flicker * brightness;
                        gl_FragColor = vec4(color, 1.0);
                    }
                `;

                // Create and compile shaders
                const vertexShader = this.createShader(this.gl.VERTEX_SHADER, vertexShaderSource);
                const fragmentShader = this.createShader(this.gl.FRAGMENT_SHADER, fragmentShaderSource);
                
                // Create program
                this.program = this.gl.createProgram();
                this.gl.attachShader(this.program, vertexShader);
                this.gl.attachShader(this.program, fragmentShader);
                this.gl.linkProgram(this.program);
                
                // Get uniform locations
                this.uniforms = {
                    time: this.gl.getUniformLocation(this.program, 'time'),
                    resolution: this.gl.getUniformLocation(this.program, 'resolution'),
                    tint: this.gl.getUniformLocation(this.program, 'tint'),
                    brightness: this.gl.getUniformLocation(this.program, 'brightness')
                };
                
                // Create geometry
                const positions = new Float32Array([
                    -1, -1,  1, -1,  -1, 1,
                    -1, 1,   1, -1,   1, 1
                ]);
                
                this.positionBuffer = this.gl.createBuffer();
                this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.positionBuffer);
                this.gl.bufferData(this.gl.ARRAY_BUFFER, positions, this.gl.STATIC_DRAW);
                
                this.startTime = Date.now();
            }

            createShader(type, source) {
                const shader = this.gl.createShader(type);
                this.gl.shaderSource(shader, source);
                this.gl.compileShader(shader);
                
                if (!this.gl.getShaderParameter(shader, this.gl.COMPILE_STATUS)) {
                    console.error('Shader compilation error:', this.gl.getShaderInfoLog(shader));
                    this.gl.deleteShader(shader);
                    return null;
                }
                
                return shader;
            }

            setupEventListeners() {
                this.resizeObserver = new ResizeObserver(() => this.resize());
                this.resizeObserver.observe(this.container);
            }

            resize() {
                const rect = this.container.getBoundingClientRect();
                this.canvas.width = rect.width * this.options.dpr;
                this.canvas.height = rect.height * this.options.dpr;
                this.canvas.style.width = rect.width + 'px';
                this.canvas.style.height = rect.height + 'px';
                
                if (this.gl) {
                    this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
                }
            }

            hexToRgb(hex) {
                let h = hex.replace("#", "");
                if (h.length === 3) h = h.split("").map((c) => c + c).join("");
                const n = parseInt(h, 16);
                return [
                    ((n >> 16) & 255) / 255,
                    ((n >> 8) & 255) / 255,
                    (n & 255) / 255
                ];
            }

            animate() {
                if (!this.gl || !this.program) {
                    requestAnimationFrame(() => this.animate());
                    return;
                }
                
                const currentTime = (Date.now() - this.startTime) / 1000 * this.options.timeScale;
                const tintRgb = this.hexToRgb(this.options.tint);
                
                this.gl.useProgram(this.program);
                
                // Set uniforms
                this.gl.uniform1f(this.uniforms.time, currentTime);
                this.gl.uniform2f(this.uniforms.resolution, this.canvas.width, this.canvas.height);
                this.gl.uniform3f(this.uniforms.tint, tintRgb[0], tintRgb[1], tintRgb[2]);
                this.gl.uniform1f(this.uniforms.brightness, this.options.brightness);
                
                // Set position attribute
                const positionAttribute = this.gl.getAttribLocation(this.program, 'position');
                this.gl.enableVertexAttribArray(positionAttribute);
                this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.positionBuffer);
                this.gl.vertexAttribPointer(positionAttribute, 2, this.gl.FLOAT, false, 0, 0);
                
                // Draw
                this.gl.clearColor(0, 0, 0, 1);
                this.gl.clear(this.gl.COLOR_BUFFER_BIT);
                this.gl.drawArrays(this.gl.TRIANGLES, 0, 6);
                
                requestAnimationFrame(() => this.animate());
            }

            updateTint(color) {
                this.options.tint = color;
            }

            destroy() {
                if (this.resizeObserver) this.resizeObserver.disconnect();
                if (this.gl) {
                    this.gl.deleteProgram(this.program);
                    this.gl.deleteBuffer(this.positionBuffer);
                }
                if (this.canvas && this.canvas.parentNode) {
                    this.canvas.parentNode.removeChild(this.canvas);
                }
            }
        }

        // Advanced Animation System
        class AdvancedAnimations {
            constructor() {
                this.initObserver();
                this.initLightCursorTrail();
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

        // Initialize everything when DOM is ready
        document.addEventListener('DOMContentLoaded', () => {
            // Initialize theme manager
            new ThemeManager();
            
            // Initialize text trail
            const textTrailContainer = document.getElementById('textTrailContainer');
            if (textTrailContainer) {
                window.textTrailInstance = new TextTrail(textTrailContainer, {
                    text: "Mydd",
                    fontFamily: "system-ui, -apple-system, sans-serif",
                    fontWeight: "900",
                    textColor: "#3b82f6"
                });
            }
            
            // Initialize faulty terminal
            const faultyTerminalContainer = document.getElementById('faultyTerminal');
            if (faultyTerminalContainer) {
                window.faultyTerminalInstance = new FaultyTerminal(faultyTerminalContainer, {
                    tint: "#3b82f6",
                    brightness: 0.6,
                    timeScale: 0.5,
                    scanlineIntensity: 0.4
                });
            }
            
            // Initialize other animations
            new AdvancedAnimations();
            new InteractionEffects();
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
            'port': 5000,
            'framework': 'Flask',
            'status': 'running'
        }
    }

def open_browser():
    """Automatically opens browser after server startup"""
    time.sleep(1.5)
    webbrowser.open(f'http://127.0.0.1:5000')

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 5000
    DEBUG = True
    
    print("🚀 Starting Flask server...")
    print(f"🔗 Server available at: http://{HOST}:{PORT}")
    print(f"🌐 Site will open automatically in your browser")
    print("🛑 To stop server: Ctrl+C")
    
    threading.Thread(target=open_browser).start()
    
    try:
        app.run(
            host=HOST, 
            port=PORT, 
            debug=DEBUG,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"⚠️ Error starting server: {e}")
        
    print("\n✅ Thank you for using Mydd Portfolio Server!")
