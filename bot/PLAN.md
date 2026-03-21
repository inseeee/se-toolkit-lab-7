# Development Plan: Telegram Bot

## Overview
Build a Telegram bot that interacts with the LMS API and Qwen LLM.

## Phase 1: Scaffold (Task 1)
- Create bot/ directory with entry point bot.py
- Implement --test mode for offline testing
- Set up handlers/ directory with placeholder commands
- Configure dependencies via pyproject.toml

## Phase 2: Commands (Task 2)
- Implement /start, /help, /health, /labs
- Connect to LMS API

## Phase 3: Intent Routing (Task 3)
- Integrate LLM for natural language queries
- Route user questions to appropriate handlers

## Phase 4: Deployment (Task 4)
- Deploy bot on VM
- Ensure stable operation
