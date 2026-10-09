from dataclasses import dataclass, field
from ipaddress import ip_address, ip_network


@dataclass
class RedEmpresarial:
    nombre: str
    cidr: str
    vlan_id: int
    gateway: str

    red: object = field(init=False)
    ip_gateway: object = field(init=False)

    def __post_init__(self):
        # Validar el identificador de la VLAN.
        if not 1 <= self.vlan_id <= 4094:
            raise ValueError("El ID de VLAN debe estar entre 1 y 4094.")

        # Interpretar y validar la red.
        red = ip_network(self.cidr, strict=True)

        if red.version != 4:
            raise ValueError("En esta primera versión solo admitimos IPv4.")

        # Interpretar y validar la puerta de enlace.
        gateway = ip_address(self.gateway)

        if gateway.version != 4:
            raise ValueError("La puerta de enlace debe ser IPv4.")

        if gateway not in red:
            raise ValueError("La puerta de enlace no pertenece a la red.")

        if gateway in (red.network_address, red.broadcast_address):
            raise ValueError(
                "La puerta de enlace no puede ser la dirección de red "
                "ni la dirección de broadcast."
            )

        self.red = red
        self.ip_gateway = gateway

@dataclass
class RegistroRedes:
    redes: list[RedEmpresarial] = field(default_factory=list)

    def agregar_red(self, nueva_red: RedEmpresarial) -> None:
        for red_existente in self.redes:
            if red_existente.vlan_id == nueva_red.vlan_id:
                raise ValueError(
                    f"La VLAN {nueva_red.vlan_id} ya está registrada "
                    f"en la red {red_existente.nombre}."
                )

            if red_existente.red == nueva_red.red:
                raise ValueError(
                    f"La red {nueva_red.red} ya está registrada "
                    f"como {red_existente.nombre}."
                )

        self.redes.append(nueva_red)

    def mostrar_redes(self) -> None:
        print("Redes registradas:")

        for red in self.redes:
            print(
                f"Nombre: {red.nombre}, "
                f"CIDR: {red.cidr}, "
                f"VLAN ID: {red.vlan_id}, "
                f"Gateway: {red.gateway}"
            )

if __name__ == "__main__":
    registro = RegistroRedes()

    gerencia = RedEmpresarial(
        nombre="GERENCIA",
        cidr="10.10.0.0/24",
        vlan_id=10,
        gateway="10.10.0.1"
    )

    desarrollo = RedEmpresarial(
        nombre="DESARROLLO",
        cidr="10.20.0.0/24",
        vlan_id=20,
        gateway="10.20.0.1"
    )

    desarrollo_duplicado = RedEmpresarial(
        nombre="DESARROLLO_DUPLICADO",
        cidr="10.30.0.0/24",
        vlan_id=10,
        gateway="10.30.0.1"
    )

    gerencia_duplicada = RedEmpresarial(
        nombre="GERENCIA_DUPLICADA",
        cidr="10.10.0.0/24",
        vlan_id=30,
        gateway="10.10.0.2"
    )

    registro.agregar_red(gerencia)
    registro.agregar_red(desarrollo)

    try:
        registro.agregar_red(desarrollo_duplicado)
    except ValueError as error:
        print(f"ERROR DE VALIDACIÓN: {error}")

    try:
        registro.agregar_red(gerencia_duplicada)
    except ValueError as error:
        print(f"ERROR DE VALIDACIÓN: {error}")

    print("\nREDES REGISTRADAS:")
    registro.mostrar_redes()