from ticket_manager import TicketManager
from bug_ticket import BugTicket
from feature_ticket import FeatureTicket


manager = TicketManager()

manager.load_tickets()


while True:

    print("\n========== Ticket Tracker ==========")
    print("1. Add Bug Ticket")
    print("2. Add Feature Ticket")
    print("3. Update Ticket Status")
    print("4. Close Ticket")
    print("5. Sort by Priority")
    print("6. Display Kanban Board")
    print("7. Exit")

    choice = input("Enter choice : ")

    # Add Bug Ticket
    if choice == "1":

        ticket_id = int(input("Ticket ID : "))
        title = input("Title : ")
        priority = input("Priority (High/Medium/Low) : ")
        status = input("Status (To Do/In Progress/Done) : ")
        severity = input("Severity : ")

        bug = BugTicket(
            ticket_id,
            title,
            priority,
            status,
            severity
        )

        manager.add_ticket(bug)
        manager.save_tickets()

        print("Bug Ticket Added Successfully.")

    # Add Feature Ticket
    elif choice == "2":

        ticket_id = int(input("Ticket ID : "))
        title = input("Title : ")
        priority = input("Priority (High/Medium/Low) : ")
        status = input("Status (To Do/In Progress/Done) : ")
        effort = input("Effort Estimate : ")

        feature = FeatureTicket(
            ticket_id,
            title,
            priority,
            status,
            effort
        )

        manager.add_ticket(feature)
        manager.save_tickets()

        print("Feature Ticket Added Successfully.")

    # Update Status
    elif choice == "3":

        ticket_id = int(input("Ticket ID : "))
        status = input("New Status : ")

        if manager.update_status(ticket_id, status):
            manager.save_tickets()
            print("Status Updated.")
        else:
            print("Ticket Not Found.")

    # Close Ticket
    elif choice == "4":

        ticket_id = int(input("Ticket ID : "))

        if manager.close_ticket(ticket_id):
            manager.save_tickets()
            print("Ticket Closed.")
        else:
            print("Ticket Not Found.")

    # Sort Tickets
    elif choice == "5":

        manager.sort_by_priority()

        print("\nTickets Sorted by Priority\n")

        for ticket in manager.tickets:
            print(ticket.summary())

    # Kanban View
    elif choice == "6":

        manager.display_kanban()

    # Exit
    elif choice == "7":

        print("Exiting Program...")
        break

    else:
        print("Invalid Choice.")