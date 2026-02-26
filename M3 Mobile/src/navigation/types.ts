export type RootStackParamList = {
  Landing: undefined;
  Onboarding: undefined;
  MindReveal: undefined;
  MainTabs: undefined;
};

export type OnboardingStackParamList = {
  PersonaSelect: undefined;
  AxisCalibration: undefined;
  ListeningImport: undefined;
  NameEntry: undefined;
};

export type MainTabParamList = {
  Mind: undefined;
  Discover: undefined;
  Live: undefined;
  Library: undefined;
  Settings: undefined;
};

export type InfoStackParamList = {
  InfoList: undefined;
  PersonaDetail: { personaId: number };
};
