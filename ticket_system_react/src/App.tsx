import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Register from './components/Register';
import Login from './components/Login';
import EventList from './events/EventList';
import Event_noSeat from './events/Event_noSeat';
import { EventProvider } from './events/EventContext'; // 引入 EventProvider
import Customer from './components/Customer';
import Order from './components/Order';
import Payment from './components/Payment';
import Admin from './admin/Admin';
import AdminEventList from './admin/AdminEventList'
import IssueTickets from './admin/IssueTickets';
import AddEvent from './admin/AddEvent';
import SearchCustomer from './admin/SearchCustomer';
import './App.css';


function App() {
  return (
    <EventProvider> {/* 在這裡包裹 EventProvider */}
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/events" element={<EventList />} />
          <Route path="/event/:id" element={<Event_noSeat />} /> {/* 設置動態路由 */}
          <Route path="/customer" element={<Customer />} />
          <Route path="/order" element={<Order />} />
          <Route path="/payment" element={<Payment />} />
          <Route path="/Admin" element={<Admin />} />
          <Route path="/Admin/myEvents" element={<AdminEventList />} />
          <Route path="/Admin/info/:eventId" element={<IssueTickets />} /> {/* Event details page */}
          <Route path="/Admin/add-event" element={<AddEvent />} />
          <Route path="/Admin/get-customer-info" element={<SearchCustomer />} />
        </Routes>
      </Router>
    </EventProvider>
  );
}

export default App;
