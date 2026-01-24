import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Users, Play } from "lucide-react";
import { toast } from "sonner";

const vrRooms = [
  {
    id: 1,
    name: "Cell City Siege",
    subject: "Biology",
    description: "Battle viruses inside a 3D cell",
    players: 12,
    maxPlayers: 20,
    icon: "🦠",
    color: "from-green-500 to-emerald-500",
  },
  {
    id: 2,
    name: "Molecule Forge",
    subject: "Chemistry",
    description: "Build molecules by bonding atoms",
    players: 8,
    maxPlayers: 15,
    icon: "⚗️",
    color: "from-purple-500 to-pink-500",
  },
  {
    id: 3,
    name: "Geometry Gladiators",
    subject: "Math",
    description: "Solve puzzles to build defenses",
    players: 15,
    maxPlayers: 25,
    icon: "📐",
    color: "from-blue-500 to-cyan-500",
  },
  {
    id: 4,
    name: "Ecosystem Quest",
    subject: "Multi-subject",
    description: "Save a virtual forest ecosystem",
    players: 18,
    maxPlayers: 30,
    icon: "🌳",
    color: "from-orange-500 to-red-500",
  },
  {
    id: 5,
    name: "Physics Playground",
    subject: "Physics",
    description: "Experiment with forces and motion",
    players: 6,
    maxPlayers: 12,
    icon: "⚛️",
    color: "from-indigo-500 to-purple-500",
  },
];

const Lounge = () => {
  const handleJoinRoom = (room: typeof vrRooms[0]) => {
    toast.success(`Joining ${room.name}... 🎮`);
  };

  return (
    <div className="pb-20 px-4 pt-6 max-w-lg mx-auto min-h-screen">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gradient mb-2">VR Lounge</h1>
        <p className="text-muted-foreground">Jump into immersive learning games</p>
      </div>

      {/* Lobby Banner */}
      <Card className="p-6 mb-6 shadow-float gradient-cyber text-center">
        <div className="text-5xl mb-3 animate-float">🎮</div>
        <h2 className="text-xl font-bold text-primary-foreground mb-2">
          Virtual Campus Lobby
        </h2>
        <p className="text-sm text-primary-foreground/80">
          Choose a portal to enter a subject's VR game world
        </p>
      </Card>

      {/* Rooms List */}
      <div className="space-y-4">
        {vrRooms.map((room) => (
          <Card
            key={room.id}
            className="p-4 shadow-card gradient-card border-border hover:border-accent/50 transition-all hover:shadow-float"
          >
            <div className="flex gap-4">
              <div
                className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${room.color} flex items-center justify-center text-4xl flex-shrink-0 shadow-lg`}
              >
                {room.icon}
              </div>
              <div className="flex-1">
                <div className="flex items-start justify-between mb-1">
                  <div>
                    <h3 className="font-bold text-foreground">{room.name}</h3>
                    <p className="text-xs text-accent">{room.subject}</p>
                  </div>
                  <div className="flex items-center gap-1 bg-accent/10 px-2 py-1 rounded-full">
                    <Users className="w-4 h-4 text-accent" />
                    <span className="text-xs font-semibold text-accent">
                      {room.players}/{room.maxPlayers}
                    </span>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground mb-3">{room.description}</p>
                <Button
                  className="w-full gradient-neon glow-cyan hover:scale-105 transition-all"
                  onClick={() => handleJoinRoom(room)}
                >
                  <Play className="w-4 h-4 mr-2" />
                  Join Room
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Earn XP Notice */}
      <Card className="p-4 mt-6 shadow-card gradient-card border-secondary/30">
        <p className="text-center text-sm text-muted-foreground">
          💎 Earn <span className="font-bold text-secondary">+50 XP</span> for each VR game
          completed!
        </p>
      </Card>
    </div>
  );
};

export default Lounge;
