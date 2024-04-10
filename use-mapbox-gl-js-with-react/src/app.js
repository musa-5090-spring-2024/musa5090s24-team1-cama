import React, { useRef, useEffect, useState } from 'react';

mapboxgl.accessToken = "pk.eyJ1IjoiY3J1c2VtLTIwMjQiLCJhIjoiY2x1dTBpNm1pMDR3ODJpcGZlbDhpODV0ZyJ9.WYCf3bI56S7DW6LKib_O4w";

export default function App() {
    const mapContainer = useRef(null);
    const map = useRef(null);
    const [lng, setLng] = useState(-70.9);
    const [lat, setLat] = useState(42.35);
    const [zoom, setZoom] = useState(9);
  
    useEffect(() => {
      if (map.current) return; // initialize map only once
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [lng, lat],
        zoom: zoom
      });
    });
  
    return (
      <div>
        <div ref={mapContainer} className="map-container" />
      </div>
    );
  }