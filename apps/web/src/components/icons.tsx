import {
  Archive, Atom, BadgeCheck, Binary, Medal, Repeat, Snowflake, Book, BookMarked, BookOpenCheck, Brain, Briefcase, Calculator, Camera, ChefHat, CircleCheckBig, Code,
  Compass, Cpu, Crosshair, Crown, Dna, Dumbbell, Earth, Eye, Factory, Feather, Flame, FlaskConical, Footprints, Gavel,
  Globe, GraduationCap, Hammer, HeartPulse, Landmark, Languages, Leaf, Library, Lightbulb, LineChart, Map, Microscope,
  Moon, Mountain, Music, Palette, PenLine, PiggyBank, Plane, Rocket, RotateCcw, Scale, Shapes, Shield, Sprout, Sun,
  Sunrise, Target, Telescope, Timer, Trophy, Waves, Wrench, Zap, type LucideIcon,
} from "lucide-react";

/** Course icons (the model picks from the same list, app/prompts.py ICONS) and achievement icons. */
const ICONS: Record<string, LucideIcon> = {
  atom: Atom, binary: Binary, book: Book, brain: Brain, briefcase: Briefcase, calculator: Calculator, camera: Camera,
  "chef-hat": ChefHat, code: Code, compass: Compass, cpu: Cpu, dna: Dna, dumbbell: Dumbbell, earth: Earth,
  factory: Factory, feather: Feather, flask: FlaskConical, gavel: Gavel, globe: Globe, "graduation-cap": GraduationCap,
  hammer: Hammer, "heart-pulse": HeartPulse, landmark: Landmark, languages: Languages, leaf: Leaf, lightbulb: Lightbulb,
  "line-chart": LineChart, map: Map, microscope: Microscope, mountain: Mountain, music: Music, palette: Palette,
  "piggy-bank": PiggyBank, plane: Plane, rocket: Rocket, scale: Scale, shield: Shield, sprout: Sprout,
  telescope: Telescope, trophy: Trophy, waves: Waves, wrench: Wrench, zap: Zap,
  footprints: Footprints, shapes: Shapes, flame: Flame, crown: Crown, target: Target, crosshair: Crosshair,
  library: Library, "book-open-check": BookOpenCheck, "book-marked": BookMarked, sun: Sun, "pen-line": PenLine,
  eye: Eye, "circle-check-big": CircleCheckBig, timer: Timer, moon: Moon, sunrise: Sunrise, "rotate-ccw": RotateCcw,
  repeat: Repeat, archive: Archive, "badge-check": BadgeCheck, medal: Medal, snowflake: Snowflake,
};

/** Library areas (app/prompts.py AREAS), with a label each. */
export const AREAS: Record<string, string> = {
  engineering: "Engineering", technology: "Technology", science: "Science", maths: "Maths", business: "Business",
  finance: "Finance", health: "Health", languages: "Languages", humanities: "Humanities", arts: "Arts",
  hobbies: "Hobbies", other: "Other",
};

const HUES = ["#5fd3ff", "#8af5c8", "#a78bfa", "#fbbf24", "#f472b6", "#60a5fa", "#2dd4bf", "#fb923c"];

export function iconFor(name: string): LucideIcon {
  return ICONS[name] ?? Book;
}

/** A stable colour per course, from its id. */
export function hueFor(id: string): string {
  let h = 0;
  for (const c of id) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return HUES[h % HUES.length];
}

export function CourseIcon({ icon, id, size = 48 }: { icon: string; id: string; size?: number }) {
  const Icon = iconFor(icon);
  const hue = hueFor(id);
  return (
    <span
      className="course-icon"
      style={{
        width: size,
        height: size,
        borderRadius: size * 0.3,
        color: hue,
        background: `radial-gradient(120% 120% at 30% 10%, color-mix(in srgb, ${hue} 32%, transparent), color-mix(in srgb, ${hue} 8%, transparent) 70%)`,
      }}
      aria-hidden="true"
    >
      <Icon strokeWidth={2} style={{ width: size * 0.48, height: size * 0.48 }} />
    </span>
  );
}
