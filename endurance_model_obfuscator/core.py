from endurance import quickstart
from endurance.core.io.files import SavedCaseFile, PowerFlowRawDataFile
from endurance.utilities.serializers import JsonSerializer
from endurance.core.modeling.case import Case
from endurance.core.modeling.all import Area, Branch, Bus, FixedShunt, InductionMachine, Load, Machine, Owner, Zone
from endurance.core.modeling.all import TwoWindingTransformer, ThreeWindingTransformer
from endurance.core.modeling.all import Node, Substation, SwitchingDevice
from endurance.core.enum import StringEnum
import string
import random


class HideableRecords(StringEnum):
    area = "area"
    branch = "branch"
    bus = "bus"
    # facts = "facts"
    fixed_shunt = "fixed_shunt"
    induction_machine = "induction_machine"
    load = "load"
    machine = "machine"
    # multi_terminal_dc = "multi_terminal_dc"
    node = "node"
    owner = "owner"
    substation = "substation"
    switching_device = "switching_device"
    three_winding_transformer = "three_winding_transformer"
    # two_terminal_dc = "two_terminal_dc"
    two_winding_transformer = "two_winding_transformer"
    # vscdc = "vscdc"
    zone = "zone"

hideable_records = [HideableRecords.area,
                    HideableRecords.branch,
                    HideableRecords.bus,
                    HideableRecords.fixed_shunt,
                    HideableRecords.induction_machine,
                    HideableRecords.load,
                    HideableRecords.machine,
                    HideableRecords.node,
                    HideableRecords.owner,
                    HideableRecords.substation,
                    HideableRecords.switching_device,
                    HideableRecords.three_winding_transformer,
                    HideableRecords.two_winding_transformer,
                    HideableRecords.zone]


class Obfuscator(object):

    @property
    def case(self):
        return self._case

    @case.setter
    def case(self, value):
        self._case = value

    def __init__(self):
        pass

    def _map(self, mapping_path, records_to_map, human_readable):
        # synchronize with the working case
        self.case = Case(autoinit=True)

        mappings = {}

        # map the data
        if HideableRecords.area in records_to_map:
            mappings[HideableRecords.area] = self._map_areas(human_readable=human_readable)
        if HideableRecords.branch in records_to_map:
            mappings[HideableRecords.branch] = self._map_branches(human_readable=human_readable)
        if HideableRecords.bus in records_to_map:
            mappings[HideableRecords.bus] = self._map_buses(human_readable=human_readable)
        if HideableRecords.fixed_shunt in records_to_map:
            mappings[HideableRecords.fixed_shunt] = self._map_fixed_shunts(human_readable=human_readable)
        if HideableRecords.load in records_to_map:
            mappings[HideableRecords.load] = self._map_loads(human_readable=human_readable)
        if HideableRecords.induction_machine in records_to_map:
            mappings[HideableRecords.induction_machine] = self._map_induction_machines(human_readable=human_readable)
        if HideableRecords.machine in records_to_map:
            mappings[HideableRecords.machine] = self._map_machines(human_readable=human_readable)
        if Node and HideableRecords.node in records_to_map:
            mappings[HideableRecords.node] = self._map_nodes(human_readable=human_readable)
        if HideableRecords.owner in records_to_map:
            mappings[HideableRecords.owner] = self._map_owners(human_readable=human_readable)
        if Substation and HideableRecords.substation in records_to_map:
            mappings[HideableRecords.substation] = self._map_substations(human_readable=human_readable)
        if SwitchingDevice and HideableRecords.switching_device in records_to_map:
            mappings[HideableRecords.switching_device] = self._map_switching_devices(human_readable=human_readable)
        if HideableRecords.three_winding_transformer in records_to_map:
            transformer_mappings = self._map_three_winding_transformers(human_readable=human_readable)
            mappings[HideableRecords.three_winding_transformer] = transformer_mappings
        if HideableRecords.two_winding_transformer in records_to_map:
            transformer_mappings = self._map_two_winding_transformers(human_readable=human_readable)
            mappings[HideableRecords.two_winding_transformer] = transformer_mappings
        if HideableRecords.zone in records_to_map:
            mappings[HideableRecords.zone] = self._map_zones(human_readable=human_readable)

        # serialize the mappings to the specified path
        JsonSerializer.serialize(mapping_path, mappings)

    def _unmap(self, mapping_path):
        # synchronize with the working case
        self.case = Case(autoinit=True)

        # deserialize the mappings from the specified path
        mappings = JsonSerializer.deserialize(mapping_path)

        # unmap the data
        if HideableRecords.area in mappings.keys():
            self._unmap_areas(mappings[HideableRecords.area])
        if HideableRecords.branch in mappings.keys():
            self._unmap_branches(mappings[HideableRecords.branch])
        if HideableRecords.bus in mappings.keys():
            self._unmap_buses(mappings[HideableRecords.bus])
        if HideableRecords.load in mappings.keys():
            self._unmap_loads(mappings[HideableRecords.load])
        if HideableRecords.fixed_shunt in mappings.keys():
            self._unmap_fixed_shunts(mappings[HideableRecords.fixed_shunt])
        if HideableRecords.induction_machine in mappings.keys():
            self._unmap_induction_machines(mappings[HideableRecords.induction_machine])
        if HideableRecords.machine in mappings.keys():
            self._unmap_machines(mappings[HideableRecords.machine])
        if HideableRecords.node in mappings.keys():
            self._unmap_nodes(mappings[HideableRecords.node])
        if HideableRecords.owner in mappings.keys():
            self._unmap_owners(mappings[HideableRecords.owner])
        if HideableRecords.substation in mappings.keys():
            self._unmap_substations(mappings[HideableRecords.substation])
        if HideableRecords.switching_device in mappings.keys():
            self._unmap_switching_devices(mappings[HideableRecords.switching_device])
        if HideableRecords.three_winding_transformer in mappings.keys():
            self._unmap_three_winding_transformers(mappings[HideableRecords.three_winding_transformer])
        if HideableRecords.two_winding_transformer in mappings.keys():
            self._unmap_two_winding_transformers(mappings[HideableRecords.two_winding_transformer])
        if HideableRecords.zone in mappings.keys():
            self._unmap_zones(mappings[HideableRecords.zone])

    #region [ areas ]

    def _map_areas(self, human_readable):

        area_mappings = []

        for area in self.case.areas:
            mapping = {"number": area.number,
                       "ceii_name": area.name}
            if human_readable:
                area.name = Obfuscator.generate_readable_id("AREA ", len(area.name), area.number)
            else:
                area.name = Obfuscator.generate_random_id(size=len(area.name))
            mapping["hidden_name"] = area.name
            area_mappings.append(mapping)

        return area_mappings

    def _unmap_areas(self, mappings):

        for mapping in mappings:
            area = Area(mapping["number"])
            area.name = mapping["ceii_name"]

    #endregion

    #region [ branches ]

    def _map_branches(self, human_readable):
        branch_mappings = []

        for branch in self.case.branches:
            mapping = {"from_bus_number": branch.from_bus_number,
                       "to_bus_number": branch.to_bus_number,
                       "ceii_id": branch.circuit_id,}
            if human_readable:
                branch.circuit_id = Obfuscator.generate_readable_id("", len(branch.circuit_id), self.case.branches.index(branch))
            else:
                branch.circuit_id = Obfuscator.generate_random_id()
            mapping["hidden_id"] = branch.circuit_id
            branch_mappings.append(mapping)

        return branch_mappings

    def _unmap_branches(self, mappings):

        for mapping in mappings:
            branch = Branch(mapping["from_bus_number"], mapping["to_bus_number"], mapping["hidden_id"])
            branch.circuit_id = mapping["ceii_id"]

    #endregion

    #region [ buses]

    def _map_buses(self, human_readable):

        bus_mappings = []

        for bus in self.case.buses:
            mapping = {"number": bus.number,
                       "ceii_name": bus.name}
            if human_readable:
                bus.name = Obfuscator.generate_readable_id("BUS  ", len(bus.name), bus.number)
            else:
                bus.name = Obfuscator.generate_random_id(size=len(bus.name))
            mapping["hidden_name"] = bus.name
            bus_mappings.append(mapping)

        return bus_mappings

    def _unmap_buses(self, mappings):

        for mapping in mappings:
            bus = Bus(mapping["number"])
            bus.name = mapping["ceii_name"]

    #endregion

    #region [ fixed_shunts ]

    def _map_fixed_shunts(self, human_readable):
        fixed_shunt_mappings = []

        for fixed_shunt in self.case.fixed_shunts:
            mapping = {"bus_number": fixed_shunt.bus_number,
                       "ceii_id": fixed_shunt.identifier}
            if human_readable:
                size = len(fixed_shunt.identifier)
                index = self.case.fixed_shunts.index(fixed_shunt)
                fixed_shunt.identifier = Obfuscator.generate_readable_id("", size, index)
            else:
                fixed_shunt.identifier = Obfuscator.generate_random_id(size=len(fixed_shunt.identifier))
            mapping["hidden_id"] = fixed_shunt.identifier
            fixed_shunt_mappings.append(mapping)

        return fixed_shunt_mappings

    def _unmap_fixed_shunts(self, mappings):

        for mapping in mappings:
            fixed_shunt = FixedShunt(mapping["bus_number"], mapping["hidden_id"])
            fixed_shunt.identifier = mapping["ceii_id"]

    #endregion

    #region [ induction_machines ]

    def _map_induction_machines(self, human_readable):
        induction_machine_mappings = []

        for induction_machine in self.case.induction_machines:
            mapping = {"bus_number": induction_machine.bus_number,
                       "ceii_id": induction_machine.identifier}
            if human_readable:
                size = len(induction_machine.identifier)
                index = self.case.induction_machines.index(induction_machine)
                induction_machine.identifier = Obfuscator.generate_readable_id("", size, index)
            else:
                induction_machine.identifier = Obfuscator.generate_random_id(size=len(induction_machine.identifier))
            mapping["hidden_id"] = induction_machine.identifier
            induction_machine_mappings.append(mapping)

        return induction_machine_mappings

    def _unmap_induction_machines(self, mappings):

        for mapping in mappings:
            induction_machine = InductionMachine(mapping["bus_number"], mapping["hidden_id"])
            induction_machine.identifier = mapping["ceii_id"]

    #endregion

    #region [ loads ]

    def _map_loads(self, human_readable):
        load_mappings = []

        for load in self.case.loads:
            mapping = {"bus_number": load.bus_number,
                       "ceii_id": load.identifier}
            if human_readable:
                load.identifier = Obfuscator.generate_readable_id("", len(load.identifier), self.case.loads.index(load))
            else:
                load.identifier = Obfuscator.generate_random_id(size=len(load.identifier))
            mapping["hidden_id"] = load.identifier
            load_mappings.append(mapping)

        return load_mappings

    def _unmap_loads(self, mappings):
        for mapping in mappings:
            load = Load(mapping["bus_number"], mapping["hidden_id"])
            load.identifier = mapping["ceii_id"]

    #endregion

    #region [ machines ]

    def _map_machines(self, human_readable):
        machine_mappings = []

        for machine in self.case.machines:
            mapping = {"bus_number": machine.bus_number,
                       "ceii_id": machine.identifier}
            if human_readable:
                size = len(machine.identifier)
                index = self.case.machines.index(machine)
                machine.identifier = Obfuscator.generate_readable_id("", size, index)
            else:
                machine.identifier = Obfuscator.generate_random_id(size=len(machine.identifier))
            mapping["hidden_id"] = machine.identifier
            machine_mappings.append(mapping)

        return machine_mappings

    def _unmap_machines(self, mappings):
        for mapping in mappings:
            machine = Machine(mapping["bus_number"], mapping["hidden_id"])
            machine.identifier = mapping["ceii_id"]

    #endregion

    #region [ nodes ]

    def _map_nodes(self, human_readable):
        node_mappings = []

        for node in self.case.nodes:
            mapping = {"number": node.number,
                       "substation_number": node.substation_number,
                       "ceii_name": node.name}
            if human_readable:
                size = len(node.name)
                index = self.case.nodes.index(node)
                node.name = Obfuscator.generate_readable_id("ND ", size, index)
            else:
                node.name = Obfuscator.generate_random_id(len(node.name))
            mapping["hidden_name"] = node.name
            node_mappings.append(mapping)

        return node_mappings

    def _unmap_nodes(self, mappings):
        for mapping in mappings:
            node = Node(mapping["number"], mapping["substation_number"])
            node.name = mapping["ceii_name"]

    #endregion

    #region [ owners ]

    def _map_owners(self, human_readable):

        owner_mappings = []

        for owner in self.case.owners:
            mapping = {"number": owner.number,
                       "ceii_name": owner.name}
            if human_readable:
                owner.name = Obfuscator.generate_readable_id("OWNER", len(owner.name), owner.number)
            else:
                owner.name = Obfuscator.generate_random_id(size=len(owner.name))
            mapping["hidden_name"] = owner.name
            owner_mappings.append(mapping)

        return owner_mappings

    def _unmap_owners(self, mappings):
        for mapping in mappings:
            owner = Owner(mapping["number"])
            owner.name = mapping["ceii_name"]

    #endregion

    #region [ substations ]

    def _map_substations(self, human_readable):
        substation_mappings = []

        for substation in self.case.substations:
            mapping = {"number": substation.number,
                       "ceii_name": substation.name,
                       "ceii_latitude": substation.latitude,
                       "ceii_longitude": substation.longitude}
            if human_readable:
                size = len(substation.name)
                index = self.case.substations.index(substation)
                substation.name = Obfuscator.generate_readable_id("SUB  ", size, index)
            else:
                substation.name = Obfuscator.generate_random_id(len(substation.name))

            substation.latitude = 0.0
            substation.longitude = 0.0
            mapping["hidden_name"] = substation.name
            mapping["hidden_latitude"] = substation.latitude
            mapping["hidden_longitude"] = substation.longitude
            substation_mappings.append(mapping)

        return substation_mappings

    def _unmap_substations(self, mappings):
        for mapping in mappings:
            substation = Substation(mapping["number"])
            substation.name = mapping["ceii_name"]
            substation.latitude = mapping["ceii_latitude"]
            substation.longitude = mapping["ceii_longitude"]


    #endregion

    #region [ switching_devices ]

    def _map_switching_devices(self, human_readable):
        switching_device_mappings = []

        for switching_device in self.case.switching_devices:
            mapping = {"from_node_number": switching_device.from_node_number,
                       "to_node_number": switching_device.to_node_number,
                       "substation_number": switching_device.substation_number,
                       "ceii_id": switching_device.identifier,
                       "ceii_name": switching_device.name}
            if human_readable:
                size = len(switching_device.identifier)
                index = self.case.switching_devices.index(switching_device)
                switching_device.identifier = Obfuscator.generate_readable_id("", size, index)
                size = len(switching_device.name)
                switching_device.name = Obfuscator.generate_readable_id("CB ", size, index)
            else:
                switching_device.identifier = Obfuscator.generate_random_id(size=len(switching_device.identifier))
                switching_device.name = Obfuscator.generate_random_id(size=len(switching_device.name))
            mapping["hidden_id"] = switching_device.identifier
            mapping["hidden_name"] = switching_device.name
            switching_device_mappings.append(mapping)

        return switching_device_mappings

    def _unmap_switching_devices(self, mappings):
        for mapping in mappings:
            substation = mapping["substation_number"]
            from_node = mapping["from_node_number"]
            to_node = mapping["to_node_number"]
            identifier = mapping["hidden_id"]
            switching_device = SwitchingDevice(substation, from_node, to_node, identifier)
            switching_device.identifier = mapping["ceii_id"]
            switching_device.name = mapping["ceii_name"]

    #endregion

    #region [ three_winding_transformers ]

    def _map_three_winding_transformers(self, human_readable):
        transformer_mappings = []

        for transformer in self.case.three_winding_transformers:
            mapping = {"from_bus_number": transformer.from_bus_number,
                       "to_bus_number": transformer.to_bus_number,
                       "third_bus_number": transformer.to_bus_number,
                       "ceii_id": transformer.circuit_id,
                       "ceii_name": transformer.name}
            if human_readable:
                size = len(transformer.circuit_id)
                index = self.case.three_winding_transformers.index(transformer)
                transformer.circuit_id = Obfuscator.generate_readable_id("", size, index)
                size = len(transformer.name)
                transformer.name = Obfuscator.generate_readable_id("TX ", size, index)
            else:
                transformer.circuit_id = Obfuscator.generate_random_id(size=len(transformer.circuit_id))
                transformer.name = Obfuscator.generate_random_id(size=len(transformer.name))
            mapping["hidden_id"] = transformer.circuit_id
            mapping["hidden_name"] = transformer.name
            transformer_mappings.append(mapping)

        return transformer_mappings

    def _unmap_three_winding_transformers(self, mappings):
        for mapping in mappings:
            from_bus_number = mapping["from_bus_number"]
            to_bus_number = mapping["to_bus_number"]
            third_bus_number = mapping["third_bus_number"]
            circuit_id = mapping["hidden_id"]
            transformer = ThreeWindingTransformer(from_bus_number, to_bus_number, third_bus_number, circuit_id)
            transformer.circuit_id = mapping["ceii_id"]
            transformer.name = mapping["ceii_name"]

    #endregion

    #region [ two_winding_transformers ]

    def _map_two_winding_transformers(self, human_readable):
        transformer_mappings = []

        for transformer in self.case.two_winding_transformers:
            mapping = {"from_bus_number": transformer.from_bus_number,
                       "to_bus_number": transformer.to_bus_number,
                       "ceii_id": transformer.circuit_id,
                       "ceii_name": transformer.name}
            if human_readable:
                size = len(transformer.circuit_id)
                index = self.case.two_winding_transformers.index(transformer)
                transformer.circuit_id = Obfuscator.generate_readable_id("", size, index)
                size = len(transformer.name)
                transformer.name = Obfuscator.generate_readable_id("TX ", size, index)
            else:
                transformer.circuit_id = Obfuscator.generate_random_id(size=len(transformer.circuit_id))
                transformer.name = Obfuscator.generate_random_id(size=len(transformer.name))
            mapping["hidden_id"] = transformer.circuit_id
            mapping["hidden_name"] = transformer.name
            transformer_mappings.append(mapping)

        return transformer_mappings

    def _unmap_two_winding_transformers(self, mappings):
        for mapping in mappings:
            from_bus_number = mapping["from_bus_number"]
            to_bus_number = mapping["to_bus_number"]
            circuit_id = mapping["hidden_id"]
            transformer = TwoWindingTransformer(from_bus_number, to_bus_number, circuit_id)
            transformer.circuit_id = mapping["ceii_id"]
            transformer.name = mapping["ceii_name"]

    #endregion

    #region [ zones ]

    def _map_zones(self, human_readable):

        zone_mappings = []

        for zone in self.case.zones:
            mapping = {"number": zone.number,
                       "ceii_name": zone.name}
            if human_readable:
                zone.name = Obfuscator.generate_readable_id("ZONE ", len(zone.name), zone.number)
            else:
                zone.name = Obfuscator.generate_random_id(size=len(zone.name))
            mapping["hidden_name"] = zone.name
            zone_mappings.append(mapping)

        return zone_mappings

    def _unmap_zones(self, mappings):
        for mapping in mappings:
            zone = Zone(mapping["number"])
            zone.name = mapping["ceii_name"]

    #endregion

    def map(self, ceii_sav_path, mapping_path, obfuscated_sav_path, records_to_map=hideable_records, human_readable=False):
        # run PSSE and load the network model containing CEII data
        quickstart(QUICKSTART_LOAD_CASE=True, QUICKSTART_CASE=ceii_sav_path)

        # map the ceii identifiers to auto-generated identifiers
        self._map(mapping_path, records_to_map, human_readable)

        # write the obfuscated data to disc
        obfuscated_sav = SavedCaseFile(obfuscated_sav_path)
        obfuscated_sav.write()

    def unmap(self, obfuscated_sav_path, mapping_path, ceii_sav_path):
        # run PSSE and load the network model containing CEII data
        quickstart(QUICKSTART_LOAD_CASE=True, QUICKSTART_CASE=obfuscated_sav_path)

        # map the auto-generated identifiers to the ceii data
        self._unmap(mapping_path)

        # create a placeholder for the resulting file.
        ceii_sav = SavedCaseFile(ceii_sav_path)

        # write the ceii file to disc
        ceii_sav.write()

    def map_raw(self, ceii_raw_path, mapping_path, obfuscated_raw_path, records_to_map=hideable_records, version="34", human_readable=False):
        # run PSSE
        quickstart(QUICKSTART_LOAD_CASE=False)

        # and load the network model containing CEII data
        ceii_raw = PowerFlowRawDataFile(ceii_raw_path)
        ceii_raw.read_version(version)

        # map the ceii identifiers to auto-generated identifiers
        self._map(mapping_path, records_to_map, human_readable)

        # write the obfuscated data to disc
        obfuscated_raw = PowerFlowRawDataFile(obfuscated_raw_path)
        obfuscated_raw.write_version(version)

    def unmap_raw(self, obfuscated_raw_path, mapping_path, ceii_raw_path, version="34"):
        # run PSSE
        quickstart(QUICKSTART_LOAD_CASE=False)

        # and load the network model containing obfuscated data
        obfuscated_raw = PowerFlowRawDataFile(obfuscated_raw_path)
        obfuscated_raw.read_version(version)

        # map the obfuscated identifiers to ceii identifiers
        self._unmap(mapping_path)

        # write the ceii data to disc
        ceii_raw = PowerFlowRawDataFile(ceii_raw_path)
        ceii_raw.write_version(version)

    @staticmethod
    def generate_random_id(size=12, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def generate_readable_id(prefix, size, index):
        prefix_length = len(prefix)
        if size <= prefix_length:
            return "ERROR"
        desired_suffix_length = size - prefix_length
        suffix = str(index)
        readable_id = prefix
        for _ in range(desired_suffix_length - len(str(index))):
            readable_id += '0'
        readable_id += suffix
        return readable_id

