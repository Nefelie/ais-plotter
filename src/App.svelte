<script lang="ts">
  import { onMount } from "svelte";
  import { Map } from "maplibre-gl";
  import { MapboxOverlay } from "@deck.gl/mapbox";
  import { ScatterplotLayer } from "@deck.gl/layers";
  import "maplibre-gl/dist/maplibre-gl.css";

  // Import the color picker components
  import ColorPicker from "svelte-awesome-color-picker";
  import Wrapper from "./Wrapper.svelte";

  let map: Map;
  let deckOverlay: MapboxOverlay;
  let allPoints: { lat: number; lon: number; MMSI: number }[][] = []; // Array of points arrays for each file
  let fileNames: string[] = []; // Store filenames of uploaded files
  let fileSelections: boolean[] = []; // Store checkbox states for each file
  let fileColors: string[] = []; // Store hex color for each file's points
  let isMapReady: boolean = false; // Track when the map is fully loaded

  // Function to update the map with selected points data
  function updateMap() {
    if (!isMapReady || !deckOverlay) return;

    // Create layers for each selected file with its respective color
    const layers = allPoints
      .map((points, index) => {
        if (!fileSelections[index]) return null; // Skip if file is not selected

        const pointData = points.map((point) => ({
          position: [point.lon, point.lat],
          MMSI: point.MMSI,
        }));

        // Convert hex color to RGB array for ScatterplotLayer
        const [r, g, b] = hexToRgb(fileColors[index]);

        return new ScatterplotLayer({
          id: `scatterplot-layer-${index}`,
          data: pointData,
          getPosition: (d: any) => d.position,
          getRadius: 1,
          getFillColor: [r, g, b, 255], // Use the selected RGB color with full opacity
          radiusMinPixels: 0.5,
        });
      })
      .filter((layer) => layer !== null); // Filter out any null layers

    deckOverlay.setProps({ layers });
  }

  // Function to convert hex color to RGB array
  function hexToRgb(hex: string): [number, number, number] {
    const bigint = parseInt(hex.slice(1), 16);
    return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255];
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
            allPoints = [...allPoints, data.points]; // Add new points array for this file
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

      // Append the new file information to the lists
      fileNames = [...fileNames, file.name];
      fileSelections = [...fileSelections, true];
      fileColors = [...fileColors, "#000000"]; // Default color is black
    }
  }

  // Reactively update the map when file selections or colors change
  $: if ((fileSelections || fileColors) && isMapReady) {
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
        interleaved: true,
        layers: [],
      });

      // Add DeckGL overlay to the map
      map.addControl(deckOverlay as unknown as maplibregl.IControl);

      isMapReady = true;
    });
  });
</script>

<div id="portal"></div>
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

    <!-- Display the list of files with their respective checkboxes and color pickers -->
    {#each fileNames as fileName, index}
      <div class="file-info">
        <input type="checkbox" bind:checked={fileSelections[index]} />
        <label for="file-checkbox">{fileName}</label>

        <!-- Color Picker for each file -->
        <ColorPicker
          components={{ wrapper: Wrapper }}
          label=""
          hex={fileColors[index]}
          on:input={(event) => {
            fileColors[index] = event.detail.hex; // Update color in HEX format
            updateMap(); // Call updateMap to reapply colors on the map
          }}
        />
      </div>
    {/each}
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
    margin-right: 10px;
  }
  .no-overflow {
    border: 3px solid black;
    overflow: hidden;
  }
</style>
