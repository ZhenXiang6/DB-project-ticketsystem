import React, { createContext, useContext, ReactNode, useState, useEffect } from "react";

interface Event {
  id: number;
  name: string;
  time: string;
  description: string;
  location: string;
}

interface EventContextType {
  events: Event[];
  getEventbyId: (id: number) => Event | undefined;
}

const EventContext = createContext<EventContextType | undefined>(undefined);

interface EventProviderProps {
  children: ReactNode;
}

export const EventProvider: React.FC<EventProviderProps> = ({ children }) => {
  const [events, setEvents] = useState<Event[]>([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8800/get_all_event_detail");
        if (response.ok) {
          const res = await response.json();
          setEvents(
            res.data.map((event: any) => ({
              id: event.e_id,
              name: event.e_name,
              time: event.e_datetime,
              category: event.c_name,
              description: `${event.c_name} organized by ${event.o_name}`, // 自定義描述
              location: event.e_location,
            }))
          );
        } else {
          console.error("Failed to fetch events");
        }
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    };

    fetchEvents();
  }, []);

  const getEventbyId = (id: number) => {
    return events.find((event) => event.id === id);
  };

  return (
    <EventContext.Provider value={{ events, getEventbyId }}>
      {children}
    </EventContext.Provider>
  );
};

export const useEvent = (): EventContextType => {
  const context = useContext(EventContext);
  if (!context) {
    throw new Error("useEvent must be used within an EventProvider");
  }
  return context;
};
