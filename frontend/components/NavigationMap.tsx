"use client";

import {
  useEffect,
  useRef,
  useState,
} from "react";

import maplibregl, {
  Map as MapLibreMap,
} from "maplibre-gl";


interface Location {

  location_id: number;

  name: string | null;

  latitude: number;

  longitude: number;

  created_at: string;
}


const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://localhost:8000";


export default function NavigationMap() {

  const mapContainer =
    useRef<HTMLDivElement | null>(null);

  const map =
    useRef<MapLibreMap | null>(null);

  const markers =
    useRef<maplibregl.Marker[]>([]);

  const [locations, setLocations] =
    useState<Location[]>([]);

  const [status, setStatus] =
    useState(
      "Click anywhere on the map to save a location."
    );


  async function loadLocations() {

    const response = await fetch(
      `${API_URL}/api/v1/locations`
    );

    if (!response.ok) {
      throw new Error(
        "Unable to load locations."
      );
    }

    const data: Location[] =
      await response.json();

    setLocations(data);
  }


  async function saveLocation(
    latitude: number,
    longitude: number
  ) {

    setStatus("Saving location...");

    const response = await fetch(
      `${API_URL}/api/v1/locations`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          name: "Map Marker",
          latitude,
          longitude,
        }),
      }
    );


    if (!response.ok) {

      setStatus(
        "Failed to save location."
      );

      return;
    }


    const saved: Location =
      await response.json();


    setLocations(
      current => [
        saved,
        ...current,
      ]
    );


    setStatus(
      `Saved marker #${saved.location_id}`
    );
  }


  useEffect(() => {

    if (!mapContainer.current) {
      return;
    }


    map.current =
      new maplibregl.Map({

        container:
          mapContainer.current,

        style:
          "https://demotiles.maplibre.org/style.json",

        center: [
          -76.86,
          39.20,
        ],

        zoom: 9,
      });


    map.current.addControl(
      new maplibregl.NavigationControl(),
      "top-right"
    );


    map.current.on(
      "click",
      async event => {

        const {
          lat,
          lng,
        } = event.lngLat;


        await saveLocation(
          lat,
          lng
        );
      }
    );


    loadLocations()
      .catch(error => {

        console.error(error);

        setStatus(
          "Unable to load saved locations."
        );
      });


    return () => {

      map.current?.remove();

      map.current = null;
    };

  }, []);


  useEffect(() => {

    if (!map.current) {
      return;
    }


    markers.current.forEach(
      marker => marker.remove()
    );


    markers.current = [];


    locations.forEach(location => {

      const popup =
        new maplibregl.Popup({
          offset: 25,
        })
        .setHTML(
          `
          <strong>
            ${location.name ?? "Location"}
          </strong>

          <br>

          Latitude:
          ${location.latitude.toFixed(6)}

          <br>

          Longitude:
          ${location.longitude.toFixed(6)}
          `
        );


      const marker =
        new maplibregl.Marker()

        .setLngLat([
          location.longitude,
          location.latitude,
        ])

        .setPopup(popup)

        .addTo(map.current!);


      markers.current.push(marker);
    });

  }, [locations]);


  return (

    <section className="map-wrapper">

      <div className="status-panel">

        <strong>
          Build Level 3
        </strong>

        <span>
          {status}
        </span>

        <span>
          Saved locations:
          {" "}
          {locations.length}
        </span>

      </div>


      <div
        ref={mapContainer}
        className="map-container"
      />

    </section>
  );
}