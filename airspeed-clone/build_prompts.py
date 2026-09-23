import re
STYLE = "Clean Aviation 3D Documentary style"
TAG = ("clean photoreal 3D render, museum-grade aircraft model, muted silver and steel-blue palette, "
       "centered composition, minimal environment, shallow depth of field, calm documentary tone, "
       "any human figure shown as a faceless matte cyan-blue low-poly mannequin, no text, no watermark, 16:9")
A = ("the Spirit of St. Louis (Ryan NYP), a 1927 single-engine high-wing monoplane with a silver-white fabric fuselage, "
     "engine-turned aluminum nose panels, a nine-cylinder radial engine with a two-blade metal propeller, a long straight "
     "strut-braced wing, fixed spoked landing gear and no front windshield")
M = "a faceless matte cyan-blue low-poly mannequin pilot in a 1920s flight jacket"
ENV = {
 "studio": ("inside a clean, empty pale-grey aircraft hangar with ribbed metal walls and a polished light-grey floor",
            "soft diffuse overhead studio lighting with gentle floor reflections"),
 "dark":   ("against a seamless dark studio backdrop fading from near-black navy (#0E1320) to deep crimson (#5A1026)",
            "single soft top spotlight with a cool rim light tracing the metal edges"),
 "ocean":  ("above a calm, endless muted steel-blue Atlantic Ocean under a pale hazy sky, no land in sight",
            "soft overcast daylight with thick atmospheric haze toward the horizon"),
 "night":  ("over a dark Atlantic Ocean at night among drifting fog banks and low cloud",
            "dim cool blue moonlight, very low contrast, soft haze"),
 "cockpit":("inside the cramped cockpit of the Spirit of St. Louis: a grey wood-grain instrument panel with period round gauges "
            "and brass fittings, a woven wicker seat, tubular steel frame, small side windows, and a solid wall where a windshield would be",
            "low-key directional light picking out the gauge glass, edges falling into shadow"),
 "archival":("presented as a black-and-white archival-style 1920s photograph in a 4:3 frame with rounded corners, heavy film grain "
            "and soft focus, floating centered on a near-black background",
            "flat period daylight, desaturated greyscale tones"),
 "map":    ("on a clean modern cartographic map of the North Atlantic with pale cream land (#F1EDE4), soft blue sea (#A9C6DA), "
            "small red city markers and thin grey country borders",
            "flat, even illumination with no shadows"),
 "field":  ("on a wide, wet 1920s grass airfield under a flat grey overcast sky",
            "soft grey overcast daylight, muted and low contrast"),
}
TAGS={
 "archival":"archival-style black-and-white 1920s photograph recreation inside the "+STYLE+" edit, heavy film grain, soft focus, rounded 4:3 panel on near-black, people seen from behind or at a distance with no identifiable faces, no text, no watermark, 16:9 frame",
 "map":"clean flat cartographic illustration inside the "+STYLE+" edit, muted cream and soft blue palette, thin black route line, small red markers, minimal labels kept illegible, no watermark, 16:9"}
B=[]
def b(text,t,subject,camera,mood,action,light=None,env=None):
    B.append(dict(text=text,t=t,subject=subject,camera=camera,mood=mood,action=action,light=light,env=env))

# ---------- BEATS ----------
b("Imagine taking off on the longest solo flight ever attempted,","ocean",
  f"{A}, flying low and alone","front three-quarter chase view at the aircraft's altitude, long lens","isolated, quietly tense","the aircraft cruises steadily over the open ocean")
b("and not being able to see where you are going.","cockpit",
  f"{M} seated in the wicker seat, facing the blank solid panel ahead","over-the-shoulder from directly behind the pilot, medium lens","claustrophobic, uneasy","the pilot stares ahead at a wall with no window")
b("No glass in front of your face. No view of the horizon.","studio",
  f"dead-on front view of {A}, the area above the engine cowling showing solid silver panels where a windshield would be","static symmetrical front view at cockpit height","clinical, puzzling","the camera holds still on the windowless nose")
b("Just a wall of metal where the windshield should be.","cockpit",
  "extreme close-up of the smooth grey-painted metal wall directly in front of the pilot's seat, rivets and panel seams visible","macro close-up, shallow depth of field","stark, confining","dust particles drift slowly in the dim light")
b("That was the cockpit of the Spirit of St. Louis.","dark",
  f"{A}, shown in full side profile","slow lateral dolly along the fuselage","reverent, iconic","the aircraft sits motionless as the camera glides past")
b("In May 1927, a 25-year-old airmail pilot named Charles Lindbergh","archival",
  "a young, lanky aviator in a leather flight jacket and jodhpurs standing beside the nose of a silver monoplane, seen from a three-quarter back angle","static, slow digital push-in","historic, nostalgic","the aviator rests one hand on the propeller blade")
b("sat behind that wall for more than a day,","cockpit",
  f"{M} slumped slightly in the wicker seat, a period pocket clock on the panel","over-the-shoulder, slightly high angle","weary, enduring","the pilot's head tilts with fatigue")
b("crossed an ocean, and landed in Paris. Alone.","map",
  "a thin black arc sweeping from New York across the Atlantic to Paris, a small silver aircraft icon at its end","slow top-down pull-back revealing the whole ocean","epic, solitary","the flight path draws itself across the map")
b("Every pilot is trained to look ahead. Every aircraft is built so they can.","studio",
  "a row of three generic 1920s biplanes and monoplanes seen nose-on, each with a clear open windscreen in front of its cockpit","static wide symmetrical shot","orderly, conventional","the aircraft stand in a neat line")
b("So why would anyone design an airplane that took that away?","dark",
  f"{A} seen dead-on from the front, perfectly centered","very slow push-in toward the windowless nose","mysterious, questioning","the propeller sits still as the camera closes in")
b("The blind cockpit was not an oversight. It was a decision.","studio",
  f"a technical x-ray view of {A}, the fuselage skin semi-transparent, revealing a large fuel tank directly ahead of the cockpit highlighted in soft red","static side view","analytical, revealing","the tank glows faintly as the skin fades to transparent")
b("And to understand it, we have to start with a prize","archival",
  "a 1920s newspaper front page on a desk, headline area blurred and unreadable, a stack of banknotes beside it","slow push-in","historic, enticing","light falls across the page")
b("that was killing the people who chased it.","ocean",
  "a lone wooden propeller blade floating on grey choppy water","high-angle static shot","somber, ominous","the blade bobs slowly on the waves",light="cold flat overcast light")
b("In 1919, a New York hotel owner named Raymond Orteig","archival",
  "a grand 1920s New York hotel facade with awnings and a doorman at the entrance","static wide shot","historic, formal","pedestrians pass the entrance")
b("offered $25,000 to the first aviator","archival",
  "a formal 1920s prize certificate with an ornate border and a neat stack of dollar notes beside it, text unreadable","slow top-down push-in","ambitious, tempting","the camera drifts across the certificate")
b("who could fly nonstop between New York and Paris.","map",
  "New York and Paris highlighted with glowing red markers, a dashed grey line connecting them across the Atlantic","slow pan from west to east","ambitious, daunting","the dashed line traces across the ocean")
b("For years, nobody could.","map",
  "the dashed line across the Atlantic fading out halfway over the ocean","static top-down","discouraging","the line dissolves mid-ocean")
b("The aircraft of the time simply could not carry enough fuel","studio",
  "a small generic 1920s biplane with an x-ray cutaway showing a tiny fuel tank, highlighted in soft red","static three-quarter view","technical, limiting","the small tank glows faintly")
b("to cover about 5,800 km without stopping.","map",
  "the full 5,800 km great-circle route from New York to Paris drawn as a thin black arc with a subtle distance bracket","slow pull-back","vast, intimidating","the arc stretches across the map")
b("By the mid-1920s, engines had improved, and the prize suddenly looked winnable.","dark",
  "a gleaming 1920s nine-cylinder air-cooled radial aircraft engine on a display stand","slow 180-degree orbit","hopeful, technical","the cylinders catch the light as the camera turns")
b("Serious teams began to form. Most of them followed the same logic.","archival",
  "a group of 1920s mechanics and aviators in overalls gathered around a large aircraft in a hangar, seen from behind","static wide shot","busy, competitive","the men lean over plans spread on a crate")
b("Bigger aircraft. Three engines instead of one.","studio",
  "a large 1920s three-engine high-wing monoplane with one engine on the nose and one under each wing, corrugated silver finish","slow dolly-in on the three engines","imposing, heavy","the three propellers sit still")
b("A crew of two, three, or four people to share the flying and the navigation.","studio",
  "four faceless matte cyan-blue low-poly mannequins in 1920s flight gear standing in a line in front of a large three-engine aircraft","static wide symmetrical shot","crowded, conventional","the mannequins stand side by side")
b("It sounded sensible. It was also deadly.","dark",
  "a large three-engine 1920s aircraft silhouette, lit from above, a faint red haze rising from beneath it","slow push-in","ominous, foreboding","the red haze grows slowly")
b("In 1926, French war hero René Fonck tried to take off from New York","field",
  "a heavily loaded large three-engine Sikorsky biplane-style 1920s aircraft rolling down a long runway, seen from the side","tracking shot alongside at ground level","strained, tense","the aircraft lumbers forward with wheels sinking",light="harsh early-morning light")
b("in a heavily loaded three-engine Sikorsky. It never left the ground cleanly.","field",
  "the large three-engine aircraft bouncing heavily at the end of a dirt runway, one wheel buckling","low-angle static shot","alarming","dust and dirt kick up around the wheels")
b("The aircraft crashed at the end of the runway and burned.","field",
  "a distant wreck of a large aircraft in a gully beyond a runway, a thick column of dark smoke rising","static wide long-lens shot","tragic, somber","smoke drifts slowly upward",light="flat grey light")
b("Two of his crew were killed.","archival",
  "two empty wooden chairs beside a hangar wall with two leather flight helmets resting on them","static medium shot","mournful","nothing moves")
b("In April 1927, two American naval aviators died","archival",
  "a large 1920s trimotor biplane parked on a grass field, two figures in naval flight gear walking toward it, seen from behind","static wide shot","somber, fateful","the figures walk toward the aircraft")
b("when their overloaded aircraft crashed during a test flight.","field",
  "a heavy biplane descending too low over marshland, nose dropping","tracking shot from the side","dire, sinking","the aircraft sinks toward the marsh")
b("That same month, Richard Byrd's three-engine Fokker flipped over during a trial landing,","field",
  "a large three-engine 1920s Fokker high-wing monoplane flipped onto its back on a grass field, wheels in the air","slow orbit around the wreck","shocking, stilled","a wheel still turns slowly")
b("injuring the men on board.","archival",
  "a few men in overalls rushing across a grass airfield toward an overturned aircraft, seen from behind","static wide shot","urgent","the men run toward the wreck")
b("Then, on May 8th, French aviators Charles Nungesser and François Coli left Paris","field",
  "a white single-engine 1920s biplane taking off from a French airfield at dawn","low front three-quarter tracking shot","hopeful, brave","the aircraft lifts off the grass",light="pale golden dawn light")
b("heading west toward New York. They were seen crossing the French coast.","ocean",
  "a small white biplane flying away from a chalky French coastline over grey sea","long-lens shot from behind the aircraft","departing, fragile","the aircraft shrinks into the haze")
b("After that, they were never seen again.","ocean",
  "an empty, calm grey ocean stretching to a featureless horizon","static wide shot","haunting, silent","nothing moves but gentle swells",light="cold overcast light")
b("Each of these aircraft was larger, heavier, and more complicated than the one before.","studio",
  "three large 1920s multi-engine aircraft lined up side by side, each bigger than the last","slow lateral dolly along the line","heavy, cumbersome","the camera passes each aircraft in turn")
b("And each one showed the same brutal truth. Over the Atlantic, weight was the enemy.","dark",
  "a large 1920s multi-engine aircraft sitting on an oversized industrial weighing scale, the needle pushed into a red zone","slow push-in on the scale needle","heavy, grim","the needle trembles in the red")
b("Lindbergh looked at the problem the opposite way.","archival",
  "a young, tall aviator in a flight jacket sitting at a drafting table with pencil sketches of a small monoplane, seen from over his shoulder","static medium shot","focused, contrarian","he pencils a note on the sketch")
b("Every extra engine was another thing that could fail.","dark",
  "three radial aircraft engines on stands, the outer two dimming and turning red","static symmetrical shot","risky, analytical","two engines fade to red, one remains silver")
b("Every extra crew member meant more weight.","studio",
  "three faceless matte cyan-blue low-poly mannequins standing on a large industrial scale","static front view","analytical","the scale needle rises as each figure glows")
b("Every extra pound meant less fuel.","dark",
  "a cutaway fuel tank beside a stack of cargo boxes, the fuel level inside the tank dropping as boxes are added","static side view","tense, calculated","the fuel level falls")
b("And fuel was the only thing that would get him to Paris.","map",
  "a thin black arc from New York to Paris with a small silver aircraft icon at its midpoint over the ocean","slow pan following the arc","determined","the icon moves toward Paris")
b("So he asked for something no other team wanted.","archival",
  "a young aviator in a flight jacket shaking hands with an engineer inside a small 1920s aircraft workshop, both seen in profile at a distance","static medium-wide shot","decisive","the two men shake hands")
b("One engine. One seat. As much fuel as the airframe could carry.","studio",
  f"{A}, fuselage semi-transparent in x-ray view: one radial engine, one wicker seat and large fuel tanks highlighted in sequence","static side view","minimalist, purposeful","engine, seat and tanks light up one after another")
b("That aircraft was the Ryan NYP, short for New York to Paris.","studio",
  f"{A}, centered, front three-quarter view","slow 90-degree orbit","iconic, proud","the aircraft sits gleaming on the polished floor")
b("Its backers were a group of businessmen from St. Louis,","archival",
  "a small group of 1920s businessmen in three-piece suits and hats standing on the steps of a city building, seen from a distance","static wide shot","civic, supportive","the men pose together")
b("and so it was given the name that would make it famous.","studio",
  f"close-up of the nose of {A}, the painted script lettering 'Spirit of St. Louis' visible on the engine-turned aluminum panel","slow dolly across the nose lettering","proud, historic","light slides across the lettering")
b("It was about 8.4 m long. It stood just under 3 m high.","studio",
  f"full side profile of {A}","static side view, orthographic feel","precise, technical","thin red measurement lines extend along its length and height")
b("Its wingspan was about 14 m,","studio",
  f"dead-on front view of {A} showing its full wingspan","static symmetrical front view","precise, technical","a thin red measurement line stretches from wingtip to wingtip")
b("stretched longer than the aircraft it was based on to help it lift a heavier load.","studio",
  f"top-down view of {A} with a faint ghosted outline of a shorter-winged earlier Ryan monoplane overlaid on it","static top-down view","comparative, analytical","the ghost outline fades as the longer wings extend")
b("It cruised at roughly 160 km/h.","ocean",
  f"{A} in steady level flight","side-on tracking shot at matching speed","steady, unhurried","the propeller blurs as the aircraft cruises")
b("Its range was designed to reach well beyond Paris,","map",
  "a thin black arc from New York to Paris continuing past Paris as a faint dashed line into central Europe","slow pan eastward","capable, generous","the dashed extension draws beyond Paris")
b("leaving a margin for headwinds, weather, and navigation errors.","ocean",
  f"{A} flying through light streaks of rain and haze","front three-quarter chase view","cautious, prepared","wisps of cloud slide past the wing",light="grey diffuse light with faint rain streaks")
b("Its service ceiling was around 16,400 ft.","ocean",
  f"{A} seen from below climbing through thin clouds","low-angle long-lens shot looking up","elevated, calm","the aircraft rises through the cloud layer",env="high above a sea of soft white clouds with a pale blue sky")
b("And its crew capacity was one.","cockpit",
  f"{M} alone in the single wicker seat, the tiny cockpit filled by his shoulders","static rear over-the-shoulder shot","solitary","the pilot sits motionless")
b("No co-pilot. No navigator. No radio. Not even a parachute.","studio",
  "four faint ghosted outlines of a co-pilot mannequin, a navigator mannequin, a radio set and a parachute pack floating beside an aircraft, each fading away","static wide shot","stripped-down, stark","each item dissolves one after another")
b("Lindbergh wanted every possible pound saved for one thing,","studio",
  f"{A} in x-ray side view with all fuel tanks highlighted in soft red","slow push-in","focused, single-minded","the tanks pulse faintly")
b("and at the front of the aircraft sat the engine that had to burn it.","studio",
  f"close-up of the nose of {A}: the nine-cylinder radial engine and two-blade propeller","slow orbit around the engine","mechanical, vital","light glints across the cylinders")
b("It was a Wright J-5C Whirlwind,","dark",
  "a Wright J-5C Whirlwind nine-cylinder radial engine isolated on a display stand, polished steel cylinders and cooling fins","slow 360-degree orbit","technical, admiring","the engine rotates on its stand")
b("a nine-cylinder air-cooled radial engine producing about 223 horsepower.","dark",
  "macro close-up of the cooling fins and pushrods of a nine-cylinder radial engine","macro lens, slow lateral dolly","precise, mechanical","the camera glides across the fins")
b("By the standards of its day, it was one of the most reliable aircraft engines available.","dark",
  "the radial engine in an exploded technical view, pistons and cylinders floating apart in perfect alignment","static front three-quarter view","engineered, trustworthy","components drift slowly apart")
b("For Lindbergh, it had to be, because there was no second engine to fall back on.","ocean",
  f"{A} flying alone over the ocean, seen directly from the front, the single engine centered","static head-on long-lens shot","precarious, tense","the propeller spins in a soft blur")
b("Behind the engine came the part of the aircraft that everything else was built around. Fuel.","studio",
  f"x-ray side view of {A}: fuselage and wing skin fade to transparent revealing the fuel system","slow push-in","revealing, central","fuel tanks glow warm red one by one")
b("The Spirit of St. Louis carried roughly 1,700 liters of gasoline,","studio",
  "a large transparent volume of amber gasoline shaped like a block, sitting beside the aircraft for scale","static wide shot","massive, surprising","the liquid gently settles")
b("spread across a nose tank, three wing tanks, and one large main tank.","studio",
  f"top-down x-ray view of {A} with a small nose tank, three wing tanks and one large main tank highlighted in soft red","static top-down view","technical, organized","each tank lights up in sequence")
b("Fully loaded, that fuel weighed more than the entire empty aircraft.","dark",
  "a balance scale with a silver 1920s monoplane on one side and a block of amber gasoline on the other, the fuel side lower","static symmetrical shot","surprising, heavy","the scale tips toward the fuel")
b("At takeoff, nearly half of everything the Spirit lifted was gasoline.","studio",
  f"{A} in x-ray side view, the lower half of the image showing a simple split bar in silver and red","static side view","striking","the red portion fills nearly half the bar")
b("Then came the strangest decision of all.","dark",
  f"{A} seen dead-on from the front, spotlit","slow push-in toward the space above the engine","mysterious","the camera closes in on the solid panel above the cowling")
b("The largest tank did not sit behind the pilot, or under the wing.","studio",
  f"x-ray side view of {A}, ghosted outlines of a tank behind the seat and under the wing, both crossed out by fading","static side view","analytical","the two ghost positions fade away")
b("It sat directly in front of the cockpit,","studio",
  f"x-ray side view of {A}: the large main fuel tank glowing red directly between the engine and the pilot's seat","slow push-in on the tank","revealing","the tank brightens")
b("filling the space where a windshield would normally be.","cockpit",
  f"{M} seen from behind, the solid wall ahead turning semi-transparent to reveal the large metal fuel tank just beyond it","over-the-shoulder, static","claustrophobic, revealing","the wall fades to show the tank")
b("Behind it, Lindbergh's cockpit was small, bare, and loud.","cockpit",
  "the empty cramped cockpit: wicker seat, control stick, rudder pedals, bare tubular frame","slow push-in from behind the seat","spartan, confining","the control stick vibrates slightly")
b("His seat was made of wicker, because wicker was light.","cockpit",
  "macro close-up of the woven wicker seat back, fine weave texture","macro lens, slow pan","simple, deliberate","light slides across the weave")
b("His maps were trimmed to remove anything he would not fly over.","cockpit",
  "a folded 1920s nautical chart with its edges cut away, resting on the pilot's knee","close-up, top-down","meticulous","a mannequin hand smooths the map")
b("His instruments were basic: a compass, an altimeter, an airspeed indicator,","cockpit",
  "the grey wood-grain instrument panel with a compass, altimeter and airspeed indicator","slow lateral dolly across the gauges, shallow depth of field","precise, vintage","each gauge comes into focus in turn")
b("a clock, and gauges for the engine.","cockpit",
  "close-up of a period panel clock and small engine gauges with brass bezels","macro lens, static","detailed, sparse","the clock's second hand ticks")
b("To see forward, he had two options.","cockpit",
  f"{M} seen from behind, turning his head toward the side window","over-the-shoulder","problem-solving","the pilot glances left")
b("He could lean out of the side windows.","ocean",
  f"side view of {A} in flight, the pilot mannequin's head leaning out of the small side window","side tracking shot close to the cockpit","awkward, determined","the pilot leans out into the wind")
b("Or he could use a small periscope that slid out from the left side of the fuselage.","studio",
  f"close-up of the left side of {A}'s fuselage at the cockpit, a small periscope tube extending outward","slow push-in on the periscope","ingenious, makeshift","the periscope slides out")
b("Both were awkward. Neither gave him a proper view.","cockpit",
  "first-person view through a small periscope eyepiece showing a narrow, blurry circular sliver of horizon","POV, static","limited, frustrating","the image wobbles slightly")
b("And that was accepted from the very beginning.","studio",
  f"{A} in front three-quarter view, centered","slow pull-back","resolute, calm","the aircraft sits still")
b("The aircraft was built by Ryan Airlines, a small company in San Diego.","archival",
  "a small 1920s aircraft factory building beside a harbor with a hand-painted sign too blurry to read","static wide shot","modest, hardworking","workers walk in and out of the doors")
b("Its chief engineer, Donald Hall, worked closely with Lindbergh,","archival",
  "two men in shirtsleeves leaning over a drafting table covered in aircraft drawings, seen from behind","static medium shot","collaborative, focused","one points at a detail on the plans")
b("often redesigning parts within hours of a conversation.","archival",
  "workers inside a 1920s workshop fitting wooden wing ribs onto a long wing spar","slow lateral pan","urgent, industrious","hands fit the ribs into place")
b("Other teams already had aircraft. Lindbergh had almost nothing.","studio",
  "a bare steel-tube fuselage frame on sawhorses in an empty workshop","slow orbit around the frame","underdog, raw","the camera circles the skeleton")
b("So Ryan built the Spirit in about 60 days.","studio",
  f"{A} assembling in time-lapse from bare frame to finished aircraft","static side view","fast, determined","fabric, wings and engine appear in sequence")
b("When it was finished, Lindbergh tested it.","ocean",
  f"{A} flying low over a sunlit Californian coastline","front three-quarter chase view","confident, fresh","the aircraft banks gently",env="above a bright Californian coastline with a pale beach and calm blue Pacific water",light="clear warm daylight")
b("Then he flew it across the United States, from San Diego to St. Louis,","map",
  "a map of the United States with a thin black line from San Diego to St. Louis and a small silver aircraft icon","slow pan eastward","bold, forward","the line draws across the continent",env="on a clean modern map of the United States with pale cream land and small red city markers")
b("and on to New York, setting a transcontinental record along the way.","map",
  "the black line continuing from St. Louis to New York, the icon arriving at New York","slow pan and zoom toward New York","triumphant","the line completes at New York",env="on a clean modern map of the United States with pale cream land and small red city markers")
b("By the time he arrived, the aircraft that had started as a sketch was ready to cross an ocean.","studio",
  f"a faint pencil blueprint of the aircraft dissolving into the finished {A}","static side view","transformative, ready","the sketch lines fill in with solid form")
b("The morning of May 20th, 1927 was grey and wet.","field",
  f"{A} parked alone on a muddy airfield, puddles around its wheels","static wide shot","heavy, anxious","light drizzle falls",light="flat grey dawn light with drizzle")
b("Rain had soaked the runway at Roosevelt Field on Long Island.","field",
  "close-up of a muddy grass runway with water pooling in tire ruts","low-angle static shot","sodden, ominous","raindrops ripple the puddles",light="grey dawn light with drizzle")
b("The Spirit was so heavy with fuel that its tires pressed into the soft ground.","field",
  f"close-up of the spoked landing gear of {A} sinking into mud","low-angle macro shot","strained, heavy","the tire presses deeper into the mud",light="grey dawn light")
b("Lindbergh opened the throttle.","cockpit",
  f"{M}'s gloved hand pushing a brass throttle lever forward","close-up, shallow depth of field","decisive, tense","the lever slides forward")
b("The aircraft rolled slowly, bouncing across the mud, far too slowly for comfort.","field",
  f"{A} rolling down a muddy runway, mud spraying from the wheels","low tracking shot alongside","strained, suspenseful","the aircraft bounces across the ground",light="grey morning light")
b("At the end of the field were telephone wires.","field",
  "a row of wooden telephone poles and sagging wires at the end of a grass field","long-lens static shot from runway level","threatening","the wires sway slightly",light="grey morning light")
b("He cleared them by only a few meters.","field",
  f"{A} passing just above a line of telephone wires, wheels almost touching","low-angle static shot looking up","breathless, near-miss","the aircraft skims over the wires",light="grey morning light")
b("The first challenge of the flight was not the ocean. It was simply getting into the air.","field",
  f"{A} climbing slowly away over wet fields and trees","long-lens shot from behind","relieved, fragile","the aircraft shrinks into the grey sky",light="grey morning light")
b("He followed the coast north, past New England, past Nova Scotia, past Newfoundland.","map",
  "a thin black line tracing north along the North American coast past New England, Nova Scotia and Newfoundland","slow pan northeast following the line","journeying","the silver aircraft icon moves along the coast")
b("Then the land ran out, and there was only water.","ocean",
  f"{A} flying away from the last rocky coastline toward open sea","high wide shot from behind","vast, lonely","the coastline slips away behind the aircraft")
b("As night fell, he flew into fog. Clouds rose around him.","night",
  f"{A} flying into a wall of fog","front three-quarter chase view","eerie, enclosing","fog swallows the wingtips")
b("At one point, ice began to form on the aircraft,","night",
  f"close-up of the leading edge of the wing of {A} with frost and ice crystals forming","macro lens, slow dolly along the wing","cold, dangerous","ice crystals spread across the fabric")
b("and he turned back and forth searching for clearer air.","night",
  f"{A} banking steeply between towering dark clouds","wide shot from slightly above","searching, tense","the aircraft tilts into a turn")
b("When he dropped low, the sea was only a short distance beneath his wheels.","night",
  f"{A} skimming just above dark rolling waves","low side-on tracking shot at wave height","perilous","spray lifts from wave crests below the wheels")
b("When he climbed, there was nothing to see at all.","night",
  f"{A} almost fully hidden inside dense grey cloud, only faint silhouette visible","static front view","disorienting, blind","cloud streams past the silhouette")
b("And through all of it, he could not see straight ahead.","cockpit",
  f"{M} seen from behind facing the solid wall, a faint darkness pressing at the side windows","over-the-shoulder, very slow push-in","claustrophobic, blind","the pilot's shoulders tense",light="very dim cool light from the side windows, deep shadows")
b("But the greatest danger was not the weather. It was sleep.","cockpit",
  f"close-up of {M}'s head nodding forward","side profile close-up, shallow depth of field","drowsy, dangerous","the head dips and jerks back up",light="very dim cool light")
b("Lindbergh had been awake for most of the day before takeoff.","archival",
  "a small 1920s hotel room at night with an untouched made bed and a lamp on","static medium shot","restless, sleepless","the lamp glows in the dark room")
b("As the hours passed, his eyes closed on their own.","cockpit",
  "the period panel clock with its hands sweeping forward rapidly","macro, static","exhausting, relentless","the clock hands spin forward",light="very dim cool light")
b("He held them open with his fingers.","cockpit",
  f"close-up side profile of {M} raising a gloved hand to his face","close-up","desperate, determined","fingers press at the eye area of the faceless head",light="very dim cool light")
b("He flew with the side window open so the cold air would hit his face.","ocean",
  f"side view of {A} at night, the small side window open with a gust of mist streaming in","side tracking shot close to the cockpit","cold, stubborn","mist blows into the cockpit",env="over a dark Atlantic Ocean at night",light="dim cool moonlight")
b("The Spirit helped in its own way. It was not especially stable.","ocean",
  f"{A} gently wandering off level, wings rocking","front head-on long-lens shot","unsteady","the wings tip slowly left and right",env="over a dark Atlantic Ocean at night",light="dim cool moonlight")
b("If Lindbergh relaxed for a moment, the aircraft started to drift,","ocean",
  f"{A} slowly dropping a wing and veering off course","wide shot from behind","slipping, uneasy","the aircraft drifts into a slow bank",env="over a dark Atlantic Ocean at night",light="dim cool moonlight")
b("and the movement forced him back awake.","cockpit",
  f"{M} snapping upright and gripping the control stick","over-the-shoulder","jolting, alert","the pilot jerks upright",light="very dim cool light")
b("A more comfortable airplane might have let him drift off entirely.","studio",
  "a generic stable 1920s passenger aircraft with a padded upholstered seat visible through an open cabin door","slow push-in on the soft seat","ironic, reflective","the soft seat sits invitingly")
b("Navigation was just as unforgiving.","ocean",
  f"{A} tiny in frame over a completely featureless ocean","extreme wide top-down shot","directionless, vast","the aircraft crawls across the empty sea",light="soft grey dawn light")
b("With no radio and no landmarks, Lindbergh used dead reckoning.","cockpit",
  "a nautical chart on the pilot's knee with a pencil and a small protractor","close-up, top-down","methodical","a mannequin hand draws a pencil line")
b("He calculated his position using his heading, his speed, the time elapsed,","cockpit",
  "the compass, airspeed indicator and clock on the wood-grain panel","slow rack focus from gauge to gauge","precise, methodical","focus shifts across the three gauges")
b("and his best estimate of the wind.","ocean",
  "close-up of white wave crests being blown sideways by wind across grey sea","high-angle shot looking down","uncertain","spray streaks sideways",light="soft grey dawn light")
b("Every hour of guesswork added to the error of the hour before.","map",
  "a flight-path arc over the Atlantic surrounded by a faint cone of uncertainty that widens toward Europe","slow push-in","mounting uncertainty","the cone widens")
b("After nearly a full day over the Atlantic, he saw fishing boats.","ocean",
  "a few small wooden fishing boats on grey water seen from above","high-angle aerial shot from the aircraft's height","hopeful, relieved","the boats bob on the swell",light="soft afternoon light breaking through haze")
b("Then a coastline. It was Ireland.","ocean",
  f"{A} approaching a green rugged Irish coastline with cliffs","front three-quarter chase view","relief, arrival","the coast emerges from the haze",env="over grey sea approaching green cliffs of the Irish coast",light="soft afternoon light through haze")
b("And when he checked his maps, he found he was only a few miles from where he had planned to be.","map",
  "the Irish coast with a planned dashed line and an actual solid black line almost overlapping","slow push-in on the two lines","vindicated, precise","the two lines converge")
b("After more than 3,000 km of open water, with no radio and no help, his estimate had held.","ocean",
  f"{A} crossing over the Irish coastline from sea to land","high wide shot from behind","triumphant, calm","the aircraft passes from water to green land",env="above the green fields and cliffs of the Irish coast",light="soft afternoon light")
b("He turned toward England, then crossed the Channel to France.","map",
  "the black flight path continuing from Ireland across southern England and the English Channel to northern France","slow pan southeast","purposeful","the silver icon moves toward France",env="on a clean modern map of Ireland, Britain and France with pale cream land and soft blue sea")
b("As darkness fell for the second time, he followed the lights to Paris.","night",
  f"{A} flying over the dark French countryside toward the distant glow of Paris","long-lens shot from behind","anticipation, hope","scattered warm village lights pass below",env="over the dark French countryside at night with a warm city glow on the horizon")
b("At Le Bourget airfield, around 100,000 people were waiting.","archival",
  "a vast crowd of 1920s men and women in hats gathered at a night airfield under floodlights, seen from behind","static wide shot","expectant, electric","the crowd presses forward")
b("Lindbergh came in to land at night, leaning out the side to see the ground he was about to touch.","night",
  f"{A} on final approach at night, pilot mannequin leaning out the side window","side tracking shot","tense, focused","the aircraft descends toward floodlit grass",env="above a floodlit grass airfield at night")
b("The Spirit came down safely.","night",
  f"{A}'s wheels touching down on floodlit grass","low-angle close-up at wheel level","relief","the tires touch and bounce lightly",env="on a floodlit grass airfield at night",light="warm floodlight glow")
b("Thirty-three and a half hours after leaving New York,","cockpit",
  "the period panel clock, hands at rest","macro, slow push-in","exhausted, complete","the clock ticks once",light="warm floodlight spilling through the side window")
b("Lindbergh had completed the first solo nonstop crossing of the Atlantic.","map",
  "the complete black arc from New York to Paris with the silver aircraft icon resting on Paris","slow pull-back to the full Atlantic","historic, triumphant","the arc glows softly")
b("The crowd rushed the aircraft so fast that souvenir hunters tore pieces of fabric from its fuselage.","archival",
  "a dense crowd surging around a silver monoplane at night, hands reaching toward its fuselage","static wide shot","chaotic, jubilant","the crowd swarms the aircraft")
b("Almost overnight, Lindbergh became one of the most famous people on Earth.","archival",
  "a 1920s ticker-tape parade on a city avenue, paper streaming down between tall buildings, an open car in the middle","static wide shot from above","euphoric, celebratory","ticker tape rains down")
b("And the aircraft became famous with him.","dark",
  f"{A} under a single spotlight","slow 180-degree orbit","iconic, reverent","the aircraft gleams as the camera circles")
b("After Paris, the Spirit was shipped home.","archival",
  "a large 1920s ocean liner at a harbor with a crated aircraft being lifted aboard by a crane","static wide shot","transitional","the crane lifts the crate")
b("Lindbergh flew it on a tour of the United States, landing in dozens of cities,","map",
  "a map of the United States covered in a looping black route connecting dozens of red city markers","slow pull-back","expansive, celebratory","the route draws itself city to city",env="on a clean modern map of the United States with pale cream land and small red city markers")
b("then on a goodwill flight through Mexico, Central America, and the Caribbean.","map",
  "a black route line looping from the United States south through Mexico, Central America and the Caribbean islands","slow pan south","friendly, far-reaching","the silver icon travels south",env="on a clean modern map of North and Central America and the Caribbean with pale cream land and soft blue sea")
b("Across the country, interest in flying surged. Airlines found new passengers. Airports were built.","archival",
  "a busy late-1920s airport with a small terminal building and passengers walking toward a trimotor airliner","static wide shot","booming, optimistic","passengers walk across the apron")
b("Aviation began to look less like a stunt and more like the future.","studio",
  f"{A} in the foreground with a faint ghosted line of later 1930s airliners behind it","slow push-in","visionary","the ghosted airliners fade in")
b("But the Spirit of St. Louis never had a career.","studio",
  f"{A} alone in the empty hangar","static wide symmetrical shot","quiet, final","nothing moves")
b("It was not modified for new roles. It never became an airliner. No production line followed it.","studio",
  f"{A} beside an empty factory assembly line with vacant jigs","slow lateral dolly along the empty line","singular, still","the camera passes empty stations")
b("On April 30th, 1928, less than a year after Paris,","ocean",
  f"{A} flying over a river and green countryside in spring","front three-quarter chase view","farewell, calm","the aircraft cruises gently",env="above a green spring landscape with a winding river",light="soft warm afternoon light")
b("Lindbergh flew it for the final time, to Washington, D.C.,","ocean",
  f"{A} flying past a distant white domed capitol building on the horizon","long-lens side view","ceremonial, closing","the aircraft passes the dome",env="above Washington, D.C. with a distant white domed capitol on the horizon",light="soft warm afternoon light")
b("and handed it to the Smithsonian Institution.","studio",
  f"{A} suspended from the ceiling of a bright museum gallery","low-angle static shot looking up","reverent, preserved","the aircraft hangs perfectly still",env="inside a bright, airy museum gallery with a high ceiling and pale walls",light="soft even museum lighting")
b("It had done the one thing it was built to do. There was nothing left to prove.","studio",
  f"{A} suspended in a museum gallery, seen from directly below","slow pull-back","complete, dignified","the aircraft recedes overhead",env="inside a bright museum gallery with a high ceiling",light="soft even museum lighting")
b("Which brings us back to the question we started with.","dark",
  f"{A} dead-on from the front, centered","slow push-in","reflective, returning","the camera closes toward the nose")
b("Why did the Spirit of St. Louis have no front window?","cockpit",
  f"{M} seen from behind facing the solid wall ahead","over-the-shoulder, static","questioning, poised","the pilot sits still")
b("Because the space in front of Lindbergh was worth more as fuel than as glass.","studio",
  f"x-ray side view of {A}, the main fuel tank in front of the cockpit glowing red, a faint ghost windshield outline fading above it","static side view","revealing, decisive","the ghost windshield fades as the tank brightens")
b("Placing the main tank there kept its weight close to the aircraft's center of gravity.","studio",
  f"x-ray side view of {A} with a small center-of-gravity marker directly beneath the main fuel tank","static side view","analytical, balanced","a thin vertical line drops from the tank to the marker")
b("As fuel was burned over the ocean, the balance of the aircraft barely changed.","studio",
  f"x-ray side view of {A}, the fuel level inside the main tank dropping while the center-of-gravity marker stays fixed","static side view","stable, clever","the fuel level lowers steadily")
b("And putting the tank ahead of the pilot, rather than behind him,","studio",
  f"x-ray side view of {A} with the engine, tank and pilot mannequin highlighted in sequence from nose to tail","slow lateral dolly","protective, logical","engine, tank and pilot light up in order")
b("meant that in a crash, Lindbergh would not be trapped between a heavy engine in front","studio",
  f"x-ray side view of {A} with a ghosted alternate layout showing the tank behind the pilot, arrows pressing inward on the seat","static side view","grim, cautionary","inward arrows pulse toward the seat")
b("and a tank of gasoline at his back.","studio",
  "the ghosted alternate layout fading out, leaving the real layout with the tank safely ahead","static side view","relieved","the alternate layout dissolves")
b("The other teams had built aircraft to be flown comfortably. Lindbergh built one to arrive.","studio",
  f"a large three-engine 1920s aircraft on the left and {A} on the right, side by side","static symmetrical wide shot","contrasting, resolute","the light dims on the large aircraft and brightens on the Spirit")
b("He could fly without seeing ahead.","cockpit",
  f"{M} seen from behind, calm hands on the stick","over-the-shoulder","confident, composed","the pilot flies steadily")
b("He had side windows, a periscope, his instruments, and years of experience flying the mail through bad weather.","archival",
  "a 1920s open-cockpit mail biplane flying through rain over farmland with a mail sack visible in the front hold","static long-lens shot","seasoned, rugged","rain streaks across the frame")
b("What he could not do was fly without fuel.","ocean",
  f"{A} flying away toward a distant horizon over empty ocean","long-lens shot from behind","stark, decisive","the aircraft shrinks into the haze")
b("A windshield would have made the flight easier.","studio",
  f"{A} with a faint ghosted windshield appearing above the nose","static front three-quarter view","hypothetical","the ghost windshield flickers in")
b("The tank made it possible.","studio",
  f"{A} with the ghost windshield fading out and the main fuel tank glowing through the skin","static front three-quarter view","resolute, final","the tank glows steady")
b("But the Spirit of St. Louis was not the only aircraft shaped by one uncompromising problem.","dark",
  f"{A} under a spotlight, slowly fading into darkness","slow pull-back","transitional, reflective","the spotlight dims")
b("Just over a decade later, the US Navy needed a fighter","dark",
  "a dark blue WWII-era Vought F4U Corsair fighter with inverted gull wings, seen dead-on from the front, emerging from darkness","slow push-in","anticipatory, powerful","the spotlight rises on the Corsair")
b("with a propeller so large it threatened to strike the deck of every carrier it landed on.","ocean",
  "a dark blue WWII Vought F4U Corsair with a huge three-blade propeller landing on a wooden aircraft-carrier deck, propeller tips close to the planks","low-angle side view at deck level","tense, powerful","the propeller spins inches above the deck",env="on the wooden flight deck of a WWII aircraft carrier at sea",light="bright hazy daylight")
b("The solution was a wing unlike any other.","dark",
  "a dark blue F4U Corsair seen dead-on from the front, its bent inverted gull wings forming a sharp W shape","static symmetrical front view","striking, curious","rim light traces the bent wings")
b("Find out why by watching our video on the F4U Corsair now.","dark",
  "a dark blue F4U Corsair in front three-quarter view, centered","slow orbit","inviting, bold","the propeller begins to turn")


# ---------- SPLIT BEATS LONGER THAN ~5s ----------
ALT={"studio":"closer detail angle, slow push-in, shallow depth of field",
     "dark":"tighter three-quarter angle, slow orbit",
     "ocean":"wide establishing shot from a higher angle, long lens",
     "night":"tight side-on tracking shot close to the fuselage",
     "cockpit":"close side-profile angle inside the cockpit, shallow depth of field",
     "archival":"tighter crop of the same photograph with a slow digital push-in",
     "map":"closer zoom on the active section of the route",
     "field":"low ground-level angle, long lens"}
def split(x):
    w=x['text'].split()
    if len(w)<=13: return [x]
    mid=len(w)/2; best=None
    for i in range(3,len(w)-2):
        if w[i-1][-1] in ',:;.': 
            if best is None or abs(i-mid)<abs(best-mid): best=i
    if best is None or abs(best-mid)>len(w)*0.3: best=round(mid)
    a=dict(x,text=' '.join(w[:best])); c=dict(x,text=' '.join(w[best:]))
    c['camera']=ALT[x['t']]; c['action']='continuing the same moment: '+x['action']
    return split(a)+split(c)
B=[dict(y,parent=pi) for pi,x in enumerate(B) for y in split(x)]

# ---------- CHECK + RENDER ----------
script=open('spirit-of-st-louis-script.md').read()
norm=lambda s:re.sub(r'\s+',' ',s).strip()
assert norm(' '.join(x['text'] for x in B))==norm(script), "coverage mismatch"
out=["# Image Prompts — Why Did the Spirit of St. Louis Have No Front Window?",
     f"Visual style: **{STYLE}**. {len(B)} beats; every script word covered, each beat ≤ ~5 s at ~2.5 words/s.",""]
for i,x in enumerate(B,1):
    env,light=ENV[x['t']]
    env=x['env'] or env; light=x['light'] or light
    wc=len(x['text'].split())
    prompt=(f"{STYLE}: {x['subject']}, {env}. Action: {x['action']}. Camera: {x['camera']}. "
            f"Lighting: {light}. Mood: {x['mood']}. Style details: {TAGS.get(x['t'],TAG)}.")
    out+= [f"## Beat {i} ({wc} words, ~{wc/2.5:.1f}s)",
           f"**[Script Segment]** \"{x['text']}\"","",
           f"**Image Prompt:** {prompt}","",
           f"- **Camera Angle:** {x['camera']}",
           f"- **Lighting:** {light}",
           f"- **Mood:** {x['mood']}",
           f"- **Action:** {x['action']}",""]
    if wc>13: print("LONG",i,wc)
open('spirit-of-st-louis-image-prompts.md','w').write('\n'.join(out))
import json
for x in B:
    e,l=ENV[x['t']]; x['env_r']=x['env'] or e; x['light_r']=x['light'] or l
json.dump(dict(style=STYLE,tag=TAG,tags=TAGS,beats=B),open('beats.json','w'),indent=1)
print(len(B),"beats")
