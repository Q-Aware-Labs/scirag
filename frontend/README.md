# 🎨 SciRAG Frontend - Neobrutalist UI

A modern, professional React frontend with neobrutalist design for the SciRAG scientific research assistant.

## ✨ Features

- **Neobrutalist Design**
  - Thick 4px black borders
  - Bold offset shadows (no blur!)
  - Dotted background pattern
  - Bright, high-contrast colors
  - Geometric, chunky components

- **Functionality**
  - Search arXiv papers
  - Select and process papers
  - Chat with RAG-powered AI
  - View paper sources
  - Real-time responses

## 🎨 Color Palette

- **Pink**: `#FE90E8` - Accent, highlights
- **Cyan**: `#C0F7FE` - Search section
- **Green**: `#99E885` - Chat, success
- **Yellow**: `#F7CB46` - Headers, CTA
- **Peach**: `#FFDCBB` - Footer, tags
- **Black**: `#000000` - Borders, text

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ installed
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will open at **http://localhost:3000**

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── SearchSection.tsx     # Paper search interface
│   │   ├── ChatSection.tsx       # Q&A chat interface
│   │   ├── PaperCard.tsx         # Individual paper display
│   │   └── PapersList.tsx        # Sidebar papers list
│   ├── api/
│   │   └── client.ts             # API communication
│   ├── App.tsx                   # Main app component
│   ├── main.tsx                  # Entry point
│   └── index.css                 # Global styles + neobrutalism
├── index.html                    # HTML entry
├── tailwind.config.js            # Tailwind + custom colors
├── vite.config.ts                # Vite configuration
└── package.json                  # Dependencies
```

## 🎯 How to Use

### 1. Search Papers

- Enter a research topic (e.g., "neural networks")
- Adjust max papers slider (1-10)
- Click "Search"
- Papers appear with titles, authors, summaries

### 2. Process Papers

- Papers are automatically selected after search
- Click "Process X Papers" button
- Wait for processing (30-60 seconds)
- Papers get indexed into the vector database

### 3. Chat

- Switch to "Chat" tab (automatically switches after processing)
- Ask questions about the papers
- Get AI-powered answers with sources
- Continue conversation with follow-ups

## 🛠️ Development

### Available Scripts

```bash
# Development server (with hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Technologies

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - API requests
- **Lucide React** - Icons

## 🎨 Design System

### Components

All components follow the neobrutalist pattern:

```tsx
// Button
<button className="btn-brutal bg-neo-yellow shadow-brutal">
  Click me
</button>

// Card
<div className="card-brutal bg-white p-4 shadow-brutal-lg">
  Content
</div>

// Input
<input className="input-brutal bg-white shadow-brutal-sm" />
```

### Shadows

- `shadow-brutal-sm` - 2px offset
- `shadow-brutal` - 4px offset (default)
- `shadow-brutal-lg` - 6px offset
- `shadow-brutal-xl` - 8px offset

### Borders

All interactive elements have `border-4 border-black`

## 🔧 Configuration

### API Endpoint

Edit `src/api/client.ts` to change the backend URL:

```typescript
const API_BASE_URL = 'http://localhost:8000/api';
```

### Colors

Edit `tailwind.config.js` to customize colors:

```javascript
colors: {
  'neo-pink': '#FE90E8',
  'neo-cyan': '#C0F7FE',
  // ... add more colors
}
```

### Dotted Background

Edit `src/index.css` to adjust the dotted pattern:

```css
body::before {
  background-size: 20px 20px;  /* Change dot spacing */
  opacity: 0.15;                /* Change dot intensity */
}
```

## 📦 Building for Production

```bash
# Build
npm run build

# Output is in dist/ folder
# Deploy to:
# - Vercel (recommended)
# - Netlify
# - GitHub Pages
# - Any static hosting
```

## 🐛 Troubleshooting

### API Connection Error

- Make sure backend is running: `uvicorn app.main:app --reload`
- Check backend is on port 8000
- Check CORS is enabled in backend

### Styling Not Working

```bash
# Rebuild Tailwind
npx tailwindcss -i ./src/index.css -o ./dist/output.css
```

### Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🎉 Next Steps

- [ ] Add user authentication
- [ ] Save conversation history
- [ ] Export chat as PDF/Markdown
- [ ] Dark mode toggle
- [ ] More color themes
- [ ] Mobile responsiveness improvements
- [ ] Animation enhancements

## 📝 Notes

- The neobrutalist design uses **no border radius** (all sharp corners)
- Shadows are **solid offsets**, never blurred
- Colors are **bright and saturated**, not pastel
- Typography is **bold and black**, never thin
- All interactive elements have **thick borders**

---

**Built with:** React + TypeScript + Vite + Tailwind + Neobrutalism ✨
