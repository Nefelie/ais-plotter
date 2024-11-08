<script lang="ts">
  import { onMount } from "svelte";
  import { Map } from "maplibre-gl";
  import { MapboxOverlay } from "@deck.gl/mapbox";
  import { ScatterplotLayer } from "@deck.gl/layers";
  import "maplibre-gl/dist/maplibre-gl.css";

  let map: Map;
  let deckOverlay: MapboxOverlay;
  let points: { lat: number; lon: number; MMSI: number }[] = [];

  // Function to update the map with points data
  function updateMap() {
    console.log("Points array:", points);

    const pointData = points.map((point) => ({
      position: [point.lon, point.lat],
      MMSI: point.MMSI,
    }));

    const scatterplotLayer = new ScatterplotLayer({
      id: "scatterplot-layer",
      data: pointData,
      getPosition: (d: any) => d.position,
      getRadius: 1,
      getFillColor: [0, 0, 0], // Black color for the points
      radiusMinPixels: 0.5,
    });

    // Update DeckGL overlay layers
    deckOverlay.setProps({
      layers: [scatterplotLayer],
    });
  }

  // Function to handle file upload and update map
  async function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input && input.files && input.files[0]) {
      const file = input.files[0];
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/upload-pickle",
          {
            method: "POST",
            body: formData,
          }
        );
        if (response.ok) {
          const data = await response.json();
          if (data && Array.isArray(data.points)) {
            points = data.points;
            updateMap();
          } else {
            console.error("The 'points' field is missing or not an array.");
          }
        } else {
          console.error("Failed to upload and process pickle file");
        }
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    }
  }

  onMount(() => {
    map = new Map({
      container: "map",
      style:
        "https://api.maptiler.com/maps/basic-v2/style.json?key=dFVEH9IaAa3jwgv9wt5D", // MapTiler style URL
      center: [10.522, 55.8566],
      zoom: 5,
    });

    map.once("load", () => {
      console.log("Map loaded successfully!");

      // Create DeckGL overlay with MapLibre map
      deckOverlay = new MapboxOverlay({
        interleaved: true, // Ensures Deck.gl layers appear under MapLibre labels
        layers: [],
      });

      // Add DeckGL overlay to the map
      map.addControl(deckOverlay as unknown as maplibregl.IControl);

      // Optionally, fetch points data from your API
      // fetchPoints();
    });
  });
</script>

<div id="container">
  <div id="sidebar">
    <h1>AIS Data Plotter</h1>
    <label for="file-upload" class="button">Upload Pickle File</label>
    <input
      id="file-upload"
      type="file"
      accept=".pkl"
      on:change={handleFileUpload}
    />
  </div>
  <div id="map"></div>
</div>

<style>
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }
  html,
  body {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
  #container {
    display: flex;
    height: 100vh;
    width: 100vw;
  }
  #sidebar {
    width: 250px;
    padding: 20px;
    background-color: #f8f9fa;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  #map {
    flex-grow: 1;
  }
  h1 {
    font-size: 1.5em;
    margin: 0 0 1em;
    color: #333;
  }
  .button {
    display: inline-block;
    padding: 8px 16px;
    margin-top: 10px;
    cursor: pointer;
    background-color: #007bff;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    text-align: center;
    text-decoration: none;
  }
  input[type="file"] {
    display: none;
  }
</style>
