export type Player = {
  id: number;
  image: string;
  full_name: string;
  position: string;
  club_team: string;
  country: string;
};

export type Card = {
  id: number;
  image: string;
  set: { name: string };
  card_number: string;
  player: Player;
  rarity: string;
  estimated_value: number;
  serial_number: string;
  created_at: string;
  updated_at: string;
};

export const mockPlayers: Player[] = [
  {
    id: 1,
    full_name: 'Lionel Messi',
    position: 'Forward',
    club_team: 'Inter Miami',
    country: 'Argentina',
    image: 'https://images.unsplash.com/photo-1521412644187-c49fa049e84d?auto=format&fit=crop&w=400&q=80',
  },
  {
    id: 2,
    full_name: 'Kylian Mbappé',
    position: 'Forward',
    club_team: 'Real Madrid',
    country: 'France',
    image: 'https://images.unsplash.com/photo-1607040233100-1a54cf2c1a81?auto=format&fit=crop&w=400&q=80',
  },
  {
    id: 3,
    full_name: 'Erling Haaland',
    position: 'Striker',
    club_team: 'Manchester City',
    country: 'Norway',
    image: 'https://images.unsplash.com/photo-1522771930-78848d9293e8?auto=format&fit=crop&w=400&q=80',
  },
  {
    id: 4,
    full_name: 'Kevin De Bruyne',
    position: 'Midfielder',
    club_team: 'Manchester City',
    country: 'Belgium',
    image: 'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&w=400&q=80',
  },
  {
    id: 5,
    full_name: 'Alexia Putellas',
    position: 'Midfielder',
    club_team: 'FC Barcelona Femeni',
    country: 'Spain',
    image: 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=400&q=80',
  },
  {
    id: 6,
    full_name: 'Jude Bellingham',
    position: 'Midfielder',
    club_team: 'Real Madrid',
    country: 'England',
    image: 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=400&q=80',
  },
  {
    id: 7,
    full_name: 'Vinícius Júnior',
    position: 'Winger',
    club_team: 'Real Madrid',
    country: 'Brazil',
    image: 'https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=400&q=80',
  },
  {
    id: 8,
    full_name: 'Mohamed Salah',
    position: 'Winger',
    club_team: 'Liverpool',
    country: 'Egypt',
    image: 'https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=401&q=80',
  },
  {
    id: 9,
    full_name: 'Ada Hegerberg',
    position: 'Striker',
    club_team: 'Olympique Lyonnais',
    country: 'Norway',
    image: 'https://images.unsplash.com/photo-1522771930-78848d9293e8?auto=format&fit=crop&w=401&q=80',
  },
];

export const mockCards: Card[] = [
  {
    id: 101,
    image: 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=500&q=80',
    set: { name: 'Legends 2024' },
    card_number: 'LM-10',
    player: mockPlayers[0],
    rarity: 'Legendary',
    estimated_value: 1200,
    serial_number: '001/500',
    created_at: '2024-03-01',
    updated_at: '2024-05-10',
  },
  {
    id: 102,
    image: 'https://images.unsplash.com/photo-1607040233100-1a54cf2c1a81?auto=format&fit=crop&w=500&q=80',
    set: { name: 'Champions 2024' },
    card_number: 'KM-07',
    player: mockPlayers[1],
    rarity: 'Epic',
    estimated_value: 900,
    serial_number: '087/750',
    created_at: '2024-04-12',
    updated_at: '2024-05-22',
  },
  {
    id: 103,
    image: 'https://images.unsplash.com/photo-1521412644187-c49fa049e84d?auto=format&fit=crop&w=500&q=80',
    set: { name: 'Golden Boot 2024' },
    card_number: 'EH-09',
    player: mockPlayers[2],
    rarity: 'Rare',
    estimated_value: 650,
    serial_number: '144/1000',
    created_at: '2024-02-25',
    updated_at: '2024-03-15',
  },
  {
    id: 104,
    image: 'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&w=500&q=80',
    set: { name: 'Assist Kings' },
    card_number: 'KDB-17',
    player: mockPlayers[3],
    rarity: 'Epic',
    estimated_value: 720,
    serial_number: '203/850',
    created_at: '2024-01-30',
    updated_at: '2024-04-01',
  },
  {
    id: 105,
    image: 'https://images.unsplash.com/photo-1518085250887-2f903c200fee?auto=format&fit=crop&w=500&q=80',
    set: { name: 'Ballon d’Or 2023' },
    card_number: 'AP-11',
    player: mockPlayers[4],
    rarity: 'Legendary',
    estimated_value: 1100,
    serial_number: '050/300',
    created_at: '2024-03-18',
    updated_at: '2024-05-05',
  },
  {
    id: 106,
    image: 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=500&q=80',
    set: { name: 'Rising Stars' },
    card_number: 'JB-05',
    player: mockPlayers[5],
    rarity: 'Rare',
    estimated_value: 580,
    serial_number: '317/1200',
    created_at: '2024-02-10',
    updated_at: '2024-04-18',
  },
  {
    id: 107,
    image: 'https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=500&q=80',
    set: { name: 'El Clásico' },
    card_number: 'VJ-20',
    player: mockPlayers[6],
    rarity: 'Epic',
    estimated_value: 760,
    serial_number: '089/900',
    created_at: '2024-03-02',
    updated_at: '2024-05-12',
  },
  {
    id: 108,
    image: 'https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=501&q=80',
    set: { name: 'Kings of Europe' },
    card_number: 'MS-11',
    player: mockPlayers[7],
    rarity: 'Epic',
    estimated_value: 640,
    serial_number: '221/950',
    created_at: '2024-01-18',
    updated_at: '2024-03-29',
  },
  {
    id: 109,
    image: 'https://images.unsplash.com/photo-1522771930-78848d9293e8?auto=format&fit=crop&w=501&q=80',
    set: { name: 'Golden Strikers' },
    card_number: 'AH-14',
    player: mockPlayers[8],
    rarity: 'Legendary',
    estimated_value: 980,
    serial_number: '033/400',
    created_at: '2024-04-04',
    updated_at: '2024-05-16',
  },
];
