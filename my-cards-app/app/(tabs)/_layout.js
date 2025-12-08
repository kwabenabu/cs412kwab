import { Tabs } from 'expo-router';

export default function Layout() {
  return (
    <Tabs>
      <Tabs.Screen name="cards_list" options={{ title: 'Cards List' }} />
      <Tabs.Screen name="players_list" options={{ title: 'Players List' }} />
      <Tabs.Screen name="card_detail" options={{ title: 'Card Detail' }} />
    </Tabs>
  );
}
