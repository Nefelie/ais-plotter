# AIS Data Plotter

AIS Data Plotter is a web application that visualizes AIS (Automatic Identification System) data for ships on an interactive map. It allows users to view ship positions on the map and dynamically upload `.pkl` files containing AIS data for visualization. The frontend is built using Svelte and MapLibre with TypeScript, and the backend is powered by FastAPI.

## Features

- **Map Visualization**: Displays ship locations on an interactive map using MapLibre GL.
- **Dynamic File Upload**: Users can upload `.pkl` files containing AIS data for live plotting on the map.
- **TypeScript Support**: The Svelte frontend is written in TypeScript, providing type safety and better code maintainability.
- **CORS Configuration**: Supports communication between frontend (Svelte + TypeScript) and backend (FastAPI) servers.
