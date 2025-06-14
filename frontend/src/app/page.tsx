import InfluencerDashboard from "./components/InfluencerDashboard";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <h1 className="text-4xl font-bold mb-8">Influencer Dashboard</h1>
      <InfluencerDashboard />
    </main>
  );
}
