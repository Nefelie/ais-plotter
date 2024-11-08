<script lang="ts">
  import { onMount } from "svelte";
  import { Map } from "maplibre-gl";
  import { MapboxOverlay } from "@deck.gl/mapbox";
  import { ScatterplotLayer } from "@deck.gl/layers";
  import "maplibre-gl/dist/maplibre-gl.css";

  let map: Map;
  let deckOverlay: MapboxOverlay;
  let points: { lat: number; lon: number; MMSI: number }[] = [];
  let fileName: string | null = null; // Store the filename of the uploaded file
  let isFileSelected: boolean = false; // Store if a file is selected
  let isMapReady: boolean = false; // Track when the map is fully loaded and ready

  // Function to update the map with points data
  function updateMap() {
    if (!isMapReady || !deckOverlay) return; // Guard clause to ensure map is ready

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

    // Add the scatterplot layer to the overlay if isFileSelected is true
    if (isFileSelected) {
      deckOverlay.setProps({
        layers: [scatterplotLayer],
      });
    } else {
      // Remove the scatterplot layer if the checkbox is unchecked
      deckOverlay.setProps({
        layers: [],
      });
    }
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

      // Set the filename and indicate that a file was selected
      fileName = file.name;
      isFileSelected = true; // Set the checkbox to be checked by default
    }
  }

  // Reactively update the map when the checkbox is checked/unchecked
  $: if (isFileSelected !== undefined && isMapReady) {
    updateMap();
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

      // Now that the map is ready, we can update the map
      isMapReady = true; // Set the flag to true indicating map is ready
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
    <!-- Always display the checkbox and filename once a file is uploaded -->
    {#if fileName}
      <div class="file-info">
        <!-- Bind the checkbox's 'checked' attribute to isFileSelected -->
        <input
          type="checkbox"
          id="file-checkbox"
          bind:checked={isFileSelected}
        />
        <label for="file-checkbox">{fileName}</label>
      </div>
    {/if}
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
  .file-info {
    margin-top: 15px;
    display: flex;
    align-items: center;
  }
  .file-info input[type="checkbox"] {
    margin-right: 10px;
  }
  .file-info label {
    font-size: 1em;
    color: #333;
  }
</style>
