import NavigationMap from "@/components/NavigationMap";

export default function Home() {
  return (
    <main>
      <header className="header">
        <div>
          <h1>GPS Navigation</h1>

          <p>
            PostgreSQL + PostGIS Navigation Platform
          </p>
        </div>
      </header>

      <NavigationMap />
    </main>
  );
}