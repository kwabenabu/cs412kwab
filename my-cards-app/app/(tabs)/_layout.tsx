  return (
    <Tabs
      screenOptions={{
        headerShown: true,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{ title: 'Home' }}
      />
      <Tabs.Screen
        name="cards_list"
        options={{ title: 'Cards' }}
      />
      <Tabs.Screen
        name="players_list"
        options={{ title: 'Players' }}
      />
      <Tabs.Screen
        name="add_card"
        options={{ title: 'Add Card' }}
      />
      <Tabs.Screen
        name="profile"
        options={{ title: 'Profile' }}
      />
    </Tabs>
  );
}
