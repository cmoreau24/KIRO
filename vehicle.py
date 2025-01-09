from dataclasses import dataclass
@dataclass 
class Vehicle:
    id: int
    is_two_tone: bool
    
    def __str__(self):
        return f"Vehicle(id={self.id}, type={'two-tone' if self.is_two_tone else 'regular'})"