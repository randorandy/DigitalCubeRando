from typing import ClassVar

from connection_data import area_doors_unpackable
from door_logic import canOpen
from item_data import items_unpackable, Items
from loadout import Loadout
from logicInterface import AreaLogicType, LocationLogicType, LogicInterface
from logic_shortcut import LogicShortcut

# TODO: There are a bunch of places where where Expert logic needed energy tanks even if they had Varia suit.
# Need to make sure everything is right in those places. 
# (They will probably work right when they're combined like this,
#  but they wouldn't have worked right when casual was separated from expert.)

# TODO: There are also a bunch of places where casual used icePod, where expert only used Ice. Is that right?

(
    CraterR, SunkenNestL, RuinedConcourseBL, RuinedConcourseTR, CausewayR,
    SporeFieldTR, SporeFieldBR, OceanShoreR, EleToTurbidPassageR, PileAnchorL,
    ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR,
    FieldAccessL, TransferStationR, CellarR, SubbasementFissureL,
    WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR,
    ElevatorToCondenserL, LoadingDockSecurityAreaL, ElevatorToWellspringL,
    NorakBrookL, NorakPerimeterTR, NorakPerimeterBL, VulnarDepthsElevatorEL,
    VulnarDepthsElevatorER, HiveBurrowL, SequesteredInfernoL,
    CollapsedPassageR, MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR,
    ThermalReservoir1R, GeneratorAccessTunnelL, ElevatorToMagmaLakeR,
    MagmaPumpAccessR, FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR,
    SporousNookL, RockyRidgeTrailL, TramToSuziIslandR
) = area_doors_unpackable

(
    Missile, Super, PowerBomb, Morph, Springball, Bombs, HiJump,
    Varia, GravitySuit, Wave, SpeedBooster, Spazer, Ice,
    Plasma, Screw, Charge, Grapple, SpaceJump, Energy, Xray #Reserve, 
) = items_unpackable

energy200 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 1
))

energy300 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 2
))
energy400 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 3
))
energy500 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 4
))
energy600 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 5
))
energy700 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 6
))
energy800 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 7
))
energy900 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 8
))
energy1000 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 9
))
energy1200 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve))  >= 11
))
energy1500 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve))  >= 14
))

missile10 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Missile) * 5 >= 10
))
missile15 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Missile) * 5 >= 15
))
missile25 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Missile) * 5 >= 25
))
missile40 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Missile) * 5 >= 40
))
missile60 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Missile) * 5 >= 60
))
super6 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Super) * 3 >= 6
))
super12 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Super) * 3 >= 12
))
super30 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Super) * 3 >= 30
))
powerBomb6 = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    loadout.count(Items.PowerBomb) >= 2
))
powerBomb9 = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    loadout.count(Items.PowerBomb) >= 3
))
powerBomb12 = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    loadout.count(Items.PowerBomb) >= 4
))
canUseBombs = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    ((Bombs in loadout) or (PowerBomb in loadout))
))
canUsePB = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (PowerBomb in loadout)
))
canBreakBlocks = LogicShortcut(lambda loadout: (
    #with bombs or screw attack, maybe without morph
    (canUseBombs in loadout) or
    (Screw in loadout)
))
pinkDoor = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (
        (Missile in loadout) or
        (Super in loadout)
        )
))
d1  = LogicShortcut(lambda loadout: (
    (
        ( #enter from left
            (pinkDoor in loadout) and
            (Morph)
        ) or
        ( #enter from below
            (HiJump in loadout) or
            (SpaceJump in loadout) or
            (SpeedBooster in loadout) or
            (
                (Morph in loadout) and
                (Springball in loadout)
            )
        ) or
        ( #enter from right
            (Super in loadout) and
            (
                (canUsePB in loadout) or
                (
                    (canBreakBlocks in loadout) and
                    (Morph in loadout)
                )
            )
        )
    ) and
    ( #exiting killing geemers
        (canUseBombs in loadout) or
        (Screw in loadout) or
        (
            (Wave in loadout) and
            (
                (Plasma in loadout) or
                (Spazer in loadout)
            )
        )
    )
))
b1 = LogicShortcut(lambda loadout: (
    (canUsePB in loadout) and
    (Grapple in loadout) and
    (pinkDoor in loadout)
))
c2 = LogicShortcut(lambda loadout: (
    (pinkDoor in loadout)
))
e1 = LogicShortcut(lambda loadout: (
    (
            (d1 in loadout) or
            (Super in loadout)
        ) and
        (
            (
                (canBreakBlocks in loadout) and
                (Morph in loadout)
            ) or
            (canUsePB in loadout)
        )
))
g1top = LogicShortcut(lambda loadout: (
    (
        (Spazer in loadout) and
        (canUseBombs in loadout)
    ) and
    ( 
        (
            (e1 in loadout) and
            (canUsePB in loadout)
        ) or
        (
            (
                (
                    (HiJump in loadout) and
                    (Springball in loadout)
                ) or
                (GravitySuit in loadout)
            ) and
            (Super in loadout) #might be another way, but here's supers
        )
    )
))
g1low = LogicShortcut(lambda loadout: (
    (g1top in loadout) and
    (Springball in loadout) and
    (canUseBombs in loadout)
))
b4 = LogicShortcut(lambda loadout: (
    (pinkDoor in loadout) and
    (
        (canUsePB in loadout) or
        (
            (Super in loadout) and
            (Missile in loadout) and
            (canUseBombs in loadout) and
            (
                (HiJump in loadout) or
                (Springball in loadout) or
                (GravitySuit in loadout)
            )
        )
    )
))
a4 = LogicShortcut(lambda loadout: (
    (pinkDoor in loadout) and
    (canUsePB in loadout) and
    (SpeedBooster in loadout)
))
a6 = LogicShortcut(lambda loadout: (
    (a4 in loadout) and
    (Super in loadout)
))
c6 = LogicShortcut(lambda loadout: (
    (a6 in loadout) and
    (
        (SpeedBooster in loadout) or
        (SpaceJump in loadout)
    )
))

area_logic: AreaLogicType = {
    "Early": {
        # using SunkenNestL as the hub for this area, so we don't need a path from every door to every other door
        # just need at least a path with sunken nest to and from every other door in the area
        ("CraterR", "SunkenNestL"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "CraterR"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "RuinedConcourseBL"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            True
            # TODO: Expert needs energy and casual doesn't? And Casual can do it with supers, but expert can't?
        ),   
    },
}


location_logic: LocationLogicType = {
    "C2 Missile": lambda loadout: (
        True
    ),
    "E2 Morph Ball": lambda loadout: (
        True
    ),
    "E2 Energy Tank": lambda loadout: (
        (canBreakBlocks in loadout) and
        (
            (Morph in loadout) or
            (Super in loadout)
        )
    ),

    "A1 Gravity Suit": lambda loadout: (
        (Super in loadout) and
        (Morph in loadout)
    ),
    "A2 Super Missile": lambda loadout: (
        (Super in loadout) and
        (Morph in loadout)
    ),
    "A3 Charge Beam": lambda loadout: (
        ( #get in
            (
                (Super in loadout) and
                (Morph in loadout)
            ) or
            (
                (pinkDoor in loadout) and
                (canUseBombs in loadout)
            )
        ) and
        ( #get out
            (Charge in loadout) or
            (Super in loadout) or
            (Spazer in loadout) or
            (Plasma in loadout) or
            (canUseBombs in loadout)
        )
    ),
    "A4 Varia Suit": lambda loadout: (
        (a4 in loadout)
    ),
    "A6 Super Missile": lambda loadout: (
        (a6 in loadout) and
        (Grapple in loadout)
    ),
    "A7 Energy Tank": lambda loadout: (
        (a6 in loadout)
    ),
    "B1 Power Bomb": lambda loadout: (
        (b1 in loadout)
    ),
    "B2 Missile": lambda loadout: (
        (pinkDoor in loadout) and
        (canUseBombs in loadout)
    ),
    "B3 Missile": lambda loadout: (
        (canUsePB in loadout) and
        (pinkDoor in loadout)
    ),
    "B4 Power Bomb": lambda loadout: (
        (canUsePB in loadout) and
        (pinkDoor in loadout)
    ),
    "B5 Xray": lambda loadout: (
        (SpeedBooster in loadout) and
        (
            (
                (b4 in loadout) and
                (canUsePB in loadout)
            )
        ) #might be more ways from the right

    ),
    "C4 Energy Tank": lambda loadout: (
        (b4 in loadout) and
        (Super in loadout) and
        (Missile in loadout)
    ),
    "C6 Plasma Beam": lambda loadout: (
        (c6 in loadout)
    ),
    "D1 Bombs": lambda loadout: (
        (d1 in loadout)
    ),
    "D1 Missile": lambda loadout: (
        (d1 in loadout)
    ),
    "D3 Space Jump": lambda loadout: (
        (b4 in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout) and
        (canUsePB in loadout)
    ),
    "D4 Super Missile": lambda loadout: (
        (b4 in loadout) and
        (Super in loadout)
    ),
    "D6 Screw Attack": lambda loadout: (
        (c6 in loadout)
    ),
    "D7 Ice Beam": lambda loadout: (
        (c6 in loadout)
    ),
    "E1 Super Missile": lambda loadout: (
        (e1 in loadout)
    ),
    "E1 Spazer": lambda loadout: (
        (e1 in loadout)
    ),
    "E3 HiJump": lambda loadout: (
        (Super in loadout) and
        (
            (HiJump in loadout) or
            (Springball in loadout) or
            (GravitySuit in loadout) or
            (b4 in loadout)
        )
    ),
    "E4 Missile": lambda loadout: (
        (canUsePB in loadout) and
        (Super in loadout) #that's all?
    ),
    "E5 Speed Booster": lambda loadout: (
        (canUsePB in loadout) and
        (Super in loadout) #can clip back out of the room ;)
    ),
    "E6 Power Bomb": lambda loadout: (
        (a6 in loadout) or
        (
            (canUsePB in loadout) and
            (Super in loadout) and
            (
                (Varia in loadout) or
                (energy200 in loadout)
            )
        )
    ),
    "E7 Power Bomb": lambda loadout: (
        (a6 in loadout) or
        (
            (canUsePB in loadout) and
            (Super in loadout) and
            (
                (Varia in loadout) or
                (energy200 in loadout)
            ) #match e6? shortcut?
        )
    ),
    "F3 Power Bomb": lambda loadout: (
        (g1low in loadout)
        #grapple right of e3?
    ),
    "F4 Energy Tank": lambda loadout: (
        (g1low in loadout) and
        (canUsePB in loadout)
    ),
    "F4 Wave Beam": lambda loadout: (
        (g1low in loadout) and
        (canUsePB in loadout)
    ),
    "G1 Springball": lambda loadout: (
        (g1top in loadout)
    ),
    "G1 Super Missile": lambda loadout: (
        (g1low in loadout) and
        (SpeedBooster in loadout)
    ),
    "G6 Grapple Beam": lambda loadout: (
        (a6 in loadout)
    ),
    "G7 Energy Tank": lambda loadout: (
        (a6 in loadout) and
        (Grapple in loadout)
    ),

}


class Expert(LogicInterface):
    area_logic: ClassVar[AreaLogicType] = area_logic
    location_logic: ClassVar[LocationLogicType] = location_logic

    @staticmethod
    def can_fall_from_spaceport(loadout: Loadout) -> bool:
        return True
