# Employee Management System

A full-stack web application for managing employee records built with **React**, **Spring Boot**, and **MySQL**. This project demonstrates CRUD (Create, Read, Update, Delete) operations in a modern web application architecture.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.x-green)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Learning Resources](#learning-resources)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## 🎯 Overview

The **Employee Management System** is a full-stack web application that allows users to perform CRUD operations on employee records. The application uses a modern architecture with React for the frontend, Spring Boot for the backend REST API, and MySQL for data persistence.

This project was developed as a learning exercise following the tutorial by [Java Guides](https://www.javaguides.net/2021/10/spring-boot-react-full-stack-web-development-tutorial.html).

---

## ✨ Features

- ✅ **View All Employees** - Display a list of all employees in a tabular format
- ✅ **Add New Employee** - Create new employee records with first name, last name, and email
- ✅ **Update Employee** - Edit existing employee information
- ✅ **Delete Employee** - Remove employee records from the database
- ✅ **Responsive Design** - Built with Bootstrap for mobile-friendly UI
- ✅ **RESTful API** - Clean and well-structured REST endpoints
- ✅ **Form Validation** - Client-side and server-side validation
- ✅ **Navigation** - React Router for seamless page navigation
- ✅ **React Hooks** - Modern functional components using hooks
- ✅ **Single Page Application** - Fast, dynamic user experience
- ✅ **CORS Enabled** - Proper cross-origin resource sharing configuration
- ✅ **Error Handling** - Custom exception handling with meaningful messages

---

## 🛠️ Technology Stack

### Backend
- **Java** 17+
- **Spring Boot** 3.x
- **Spring Data JPA** - For database operations
- **Hibernate** - ORM framework
- **MySQL** - Relational database
- **Lombok** - To reduce boilerplate code
- **Maven** - Dependency management

### Frontend
- **React** 18.2.0
- **React Hooks** - useState, useEffect, useParams, useNavigate
- **React Router DOM** 6.10.0
- **Axios** 1.3.6 - For HTTP requests
- **Bootstrap** 5.2.3 - UI framework
- **NPM** - Package manager

---

## 🎣 React Hooks Used

This project extensively uses React Hooks to manage state and side effects in functional components:

### 1. **useState Hook**
Used to manage component state in functional components:
- `firstName`, `lastName`, `email` - Form input states
- `employees` - Array of employee objects

```javascript
const [firstName, setFirstName] = useState('')
const [employees, setEmployees] = useState([])
```

### 2. **useEffect Hook**
Used for side effects like API calls (similar to `componentDidMount` in class components):
```javascript
useEffect(() => {
    getAllEmployees();
}, [])
```

### 3. **useParams Hook**
Used to access URL parameters (e.g., employee ID from the route):
```javascript
const { id } = useParams();
```

### 4. **useNavigate Hook** (formerly useHistory)
Used for programmatic navigation between pages:
```javascript
const navigate = useNavigate();
navigate('/employees');
```

---

## 🏗️ System Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  React Frontend │────────▶│  Spring Boot    │────────▶│   MySQL         │
│  (Port 3000)    │  HTTP   │  REST API       │  JDBC   │   Database      │
│                 │◀────────│  (Port 8080)    │◀────────│                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

### Application Flow
1. User interacts with React frontend
2. React components make HTTP requests via Axios
3. Spring Boot REST controllers handle requests
4. Service layer processes business logic
5. Spring Data JPA repositories interact with MySQL
6. Data is returned through the same path back to the user

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Java Development Kit (JDK)** 17 or higher
- **Node.js** 14.x or higher
- **npm** 6.x or higher
- **MySQL** 8.x or higher
- **Maven** 3.x or higher
- **Git** (for cloning the repository)
- An IDE like **IntelliJ IDEA**, **Eclipse**, or **VS Code**

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SaiTejaReddyYeldandi/React_Spring_Employment_Management.git
cd React_Spring_Employment_Management
```

### 2️⃣ Database Setup

1. Start your MySQL server
2. Create a new database:

```sql
CREATE DATABASE ems;
```

3. Update database credentials in `application.properties`:

```properties
# src/main/resources/application.properties
spring.datasource.url=jdbc:mysql://localhost:3306/ems?useSSL=false
spring.datasource.username=root
spring.datasource.password=YOUR_PASSWORD

spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect
spring.jpa.hibernate.ddl-auto=update
```

> ⚠️ **Important**: Replace `YOUR_PASSWORD` with your actual MySQL password

---

### 3️⃣ Backend Setup

#### Create Spring Boot Project Structure

1. **Create the following packages** in your Spring Boot project:
   - `model` - JPA entities
   - `repository` - Spring Data JPA repositories
   - `controller` - REST controllers
   - `exception` - Custom exceptions
   - `dto` - Data Transfer Objects
   - `mapper` - Entity-DTO mappers

#### Configure Application Properties

Navigate to `src/main/resources/application.properties` and add:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/ems?useSSL=false
spring.datasource.username=root
spring.datasource.password=YOUR_PASSWORD

spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect
spring.jpa.hibernate.ddl-auto=update
```

> ⚠️ **Important**: 
> - Replace `YOUR_PASSWORD` with your actual MySQL password
> - For production, use `spring.jpa.hibernate.ddl-auto=validate` instead of `update`

#### Run the Backend Application

```bash
# Using Maven wrapper
./mvnw clean install
./mvnw spring-boot:run

# Or using Maven directly
mvn clean install
mvn spring-boot:run
```

Or if you're using an IDE:
- Import the project as a Maven project
- Run the main application class (usually `Application.java` or `EmsApplication.java`)

The backend server will start on `http://localhost:8080`

**Verify Backend is Running:**
```bash
curl http://localhost:8080/api/v1/employees
```

---

### 4️⃣ Frontend Setup

#### Create React Application

```bash
# Navigate to your projects directory
cd your-projects-folder

# Create React application using Create React App
npx create-react-app react-hooks-frontend

# Navigate into the project
cd react-hooks-frontend
```

#### Install Required Dependencies

```bash
# Install Bootstrap for styling
npm install bootstrap --save

# Install Axios for HTTP requests
npm install axios --save

# Install React Router for navigation
npm install react-router-dom --save
```

#### Import Bootstrap in Your Application

Open `src/index.js` and add the following import at the top:

```javascript
import 'bootstrap/dist/css/bootstrap.min.css';
```

#### Start the Development Server

```bash
npm start
```

The React application will start on `http://localhost:3000`

**Project Structure After Setup:**
```
react-hooks-frontend/
├── node_modules/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── ListEmployeeComponent.js
│   │   ├── EmployeeComponent.js
│   │   ├── HeaderComponent.js
│   │   └── FooterComponent.js
│   ├── services/
│   │   └── EmployeeService.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

---

## 🔧 Backend Implementation Details

### Employee Entity (JPA)

```java
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "employees")
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(name = "first_name")
    private String firstName;

    @Column(name = "last_name")
    private String lastName;

    @Column(name = "email_id")
    private String email;
}
```

### Employee Repository

```java
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    // All CRUD methods inherited from JpaRepository
}
```

### CORS Configuration

The backend uses `@CrossOrigin("*")` annotation to allow requests from any origin:

```java
@CrossOrigin("*")
@RestController
@RequestMapping("/api/v1/employees")
public class EmployeeController {
    // REST endpoints
}
```

### Custom Exception Handling

```java
@ResponseStatus(value = HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/employees` | Get all employees |
| `GET` | `/api/v1/employees/{id}` | Get employee by ID |
| `POST` | `/api/v1/employees` | Create new employee |
| `PUT` | `/api/v1/employees/{id}` | Update employee |
| `DELETE` | `/api/v1/employees/{id}` | Delete employee |

### Sample API Request/Response

**Create Employee (POST)**
```json
// Request Body
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com"
}

// Response (201 Created)
{
  "id": 1,
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com"
}
```

**Get All Employees (GET)**
```json
// Response (200 OK)
[
  {
    "id": 1,
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com"
  },
  {
    "id": 2,
    "firstName": "Jane",
    "lastName": "Smith",
    "email": "jane.smith@example.com"
  }
]
```

---

## ⚛️ React Components Implementation

### Employee Service (Axios)

```javascript
import axios from 'axios'

const EMPLOYEE_BASE_REST_API_URL = 'http://localhost:8080/api/v1/employees';

export const listEmployees = () => {
    return axios.get(EMPLOYEE_BASE_REST_API_URL)
};

export const createEmployee = (employee) => {
    return axios.post(EMPLOYEE_BASE_REST_API_URL, employee)
}

export const getEmployeeById = (employeeId) => {
    return axios.get(EMPLOYEE_BASE_REST_API_URL + '/' + employeeId);
}

export const updateEmployee = (employeeId, employee) => {
    return axios.put(EMPLOYEE_BASE_REST_API_URL + '/' + employeeId, employee);
}

export const deleteEmployee = (employeeId) => {
    return axios.delete(EMPLOYEE_BASE_REST_API_URL + '/' + employeeId);
}
```

### List Employee Component (with Hooks)

```javascript
const ListEmployeeComponent = () => {
    const [employees, setEmployees] = useState([])
    const navigate = useNavigate()

    useEffect(() => {
        getAllEmployees();
    }, [])

    const getAllEmployees = () => {
        listEmployees().then((response) => {
            setEmployees(response.data)
        }).catch(error => {
            console.log(error);
        })
    }

    const removeEmployee = (employeeId) => {
       deleteEmployee(employeeId).then((response) => {
            getAllEmployees();
       }).catch(error => {
           console.log(error);
       })
    }

    // JSX rendering code...
}
```

### Add/Update Employee Component

```javascript
const EmployeeComponent = () => {
    const [firstName, setFirstName] = useState('')
    const [lastName, setLastName] = useState('')
    const [email, setEmail] = useState('')
    
    const navigate = useNavigate();
    const {id} = useParams();

    const saveOrUpdateEmployee = (e) => {
        e.preventDefault();
        const employee = {firstName, lastName, email}

        if(id) {
            updateEmployee(id, employee).then((response) => {
                navigate('/employees')
            }).catch(error => {
                console.log(error)
            })
        } else {
            createEmployee(employee).then((response) => {
                navigate('/employees');
            }).catch(error => {
                console.log(error)
            })
        }
    }

    useEffect(() => {
        if(id) {
            getEmployeeById(id).then((response) => {
                setFirstName(response.data.firstName)
                setLastName(response.data.lastName)
                setEmail(response.data.email)
            }).catch(error => {
                console.log(error)
            })
        }
    }, [id])

    // Form JSX code...
}
```

### React Router Configuration (App.js)

```javascript
function App() {
  return (
    <div>
      <BrowserRouter>
        <HeaderComponent />
        <div className="container">
          <Routes>
              <Route path="/" element={<ListEmployeeComponent />}></Route>
              <Route path="/employees" element={<ListEmployeeComponent />}></Route>
              <Route path="/add-employee" element={<EmployeeComponent />}></Route>
              <Route path="/edit-employee/:id" element={<EmployeeComponent />}></Route>
            </Routes>
        </div>
        <FooterComponent />
      </BrowserRouter>
    </div>
  );
}
```

---

## 📁 Project Structure

### Backend Structure
```
src/
├── main/
│   ├── java/
│   │   └── com/yourpackage/
│   │       ├── controller/
│   │       │   └── EmployeeController.java
│   │       ├── service/
│   │       │   ├── EmployeeService.java
│   │       │   └── EmployeeServiceImpl.java
│   │       ├── repository/
│   │       │   └── EmployeeRepository.java
│   │       ├── model/
│   │       │   └── Employee.java
│   │       ├── dto/
│   │       │   └── EmployeeDto.java
│   │       ├── mapper/
│   │       │   └── EmployeeMapper.java
│   │       ├── exception/
│   │       │   └── ResourceNotFoundException.java
│   │       └── Application.java
│   └── resources/
│       └── application.properties
└── test/
```

### Frontend Structure
```
ems-frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── ListEmployeeComponent.js
│   │   ├── EmployeeComponent.js
│   │   ├── HeaderComponent.js
│   │   └── FooterComponent.js
│   ├── services/
│   │   └── EmployeeService.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

---

## 🔄 Development Workflow

### Backend Development Steps

1. **Create Spring Boot Project** using Spring Initializr
2. **Add Dependencies**: Spring Web, Spring Data JPA, MySQL Driver, Lombok
3. **Configure Database** in `application.properties`
4. **Create JPA Entity** (`Employee.java`)
5. **Create Repository** interface extending `JpaRepository`
6. **Create DTO and Mapper** classes
7. **Create Service Layer** (interface and implementation)
8. **Create REST Controller** with CRUD endpoints
9. **Add CORS Configuration** using `@CrossOrigin`
10. **Test APIs** using Postman

### Frontend Development Steps

1. **Create React App** using `create-react-app`
2. **Install Dependencies**: Bootstrap, Axios, React Router
3. **Create Components** folder structure
4. **Create Service Layer** for API calls
5. **Implement List Component** with `useState` and `useEffect`
6. **Implement Add/Edit Component** with form handling
7. **Configure Routing** in App.js
8. **Add Header and Footer** components
9. **Style with Bootstrap** CSS classes
10. **Test Complete Flow** in browser

### Key Development Points

- ✅ Use **functional components** with React Hooks (not class components)
- ✅ **useState** for state management
- ✅ **useEffect** for API calls (runs once on component mount)
- ✅ **useParams** to get route parameters
- ✅ **useNavigate** for programmatic navigation
- ✅ **Axios** for all HTTP requests
- ✅ **Promise handling** with `.then()` and `.catch()`
- ✅ **Bootstrap classes** for styling
- ✅ **React Router** for navigation
- ✅ **Single component** for both Add and Update operations

---

## 💻 Usage

### Adding an Employee
1. Navigate to `http://localhost:3000`
2. Click on the **"Add Employee"** button
3. Fill in the employee details:
   - First Name
   - Last Name
   - Email
4. Click **"Submit"** to save the employee

### Updating an Employee
1. From the employee list, click the **"Update"** button next to an employee
2. Modify the employee details in the form
3. Click **"Submit"** to save changes

### Deleting an Employee
1. From the employee list, click the **"Delete"** button next to an employee
2. The employee will be removed from the database and the list will refresh

### Viewing All Employees
- The home page (`/employees`) displays all employees in a table format
- Shows Employee ID, First Name, Last Name, and Email for each employee

---

## 📸 Screenshots

### Employee List Page
```
+----------------------------------------------------------+
| Employee Management Application                          |
+----------------------------------------------------------+
| [Add Employee]                                           |
|                                                          |
| ID | First Name | Last Name | Email        | Actions    |
|----|------------|-----------|--------------|------------|
| 1  | John       | Doe       | john@ex.com  | Edit Delete|
| 2  | Jane       | Smith     | jane@ex.com  | Edit Delete|
+----------------------------------------------------------+
| All Rights Reserved 2021 @JavaGuides                     |
+----------------------------------------------------------+
```

### Add/Edit Employee Page
```
+----------------------------------------------------------+
| Employee Management Application                          |
+----------------------------------------------------------+
|                                                          |
|  Add Employee / Update Employee                          |
|  +--------------------------------------------------+    |
|  | First Name: [________________]                   |    |
|  | Last Name:  [________________]                   |    |
|  | Email:      [________________]                   |    |
|  |                                                  |    |
|  | [Submit] [Cancel]                                |    |
|  +--------------------------------------------------+    |
|                                                          |
+----------------------------------------------------------+
| All Rights Reserved 2021 @JavaGuides                     |
+----------------------------------------------------------+
```

---

## 📚 Learning Resources

This project was built following the comprehensive tutorial from **Ramesh Fadatare** at Java Guides:

### Tutorial & Video
- **Written Tutorial**: [Spring Boot + React Full Stack Development](https://www.javaguides.net/2021/10/spring-boot-react-full-stack-web-development-tutorial.html)
- **YouTube Video**: [React Hooks + Spring Boot Full Stack Course](https://www.youtube.com/c/javaguides) - Search for "React Hooks Spring Boot"
- **Author**: Ramesh Fadatare
- **Channel**: Java Guides (178K+ subscribers)

### What This Course Teaches

#### Backend (Spring Boot)
- ✅ Creating REST APIs with Spring Boot 3+
- ✅ Using Spring Data JPA with MySQL
- ✅ Implementing CRUD operations
- ✅ Exception handling with custom exceptions
- ✅ Using Lombok to reduce boilerplate code
- ✅ Configuring CORS for frontend access
- ✅ Using IntelliJ IDEA for development
- ✅ Testing APIs with Postman

#### Frontend (React with Hooks)
- ✅ Creating React application with Create React App
- ✅ Using React Hooks (`useState`, `useEffect`, `useParams`, `useNavigate`)
- ✅ Building functional components (not class components)
- ✅ Using Axios for HTTP requests
- ✅ Implementing React Router for navigation
- ✅ Form handling in React
- ✅ Bootstrap integration for styling
- ✅ Component reusability (single component for Add/Update)

### Key Concepts Covered

1. **React Hooks**:
   - `useState` - State management in functional components
   - `useEffect` - Side effects and lifecycle methods
   - `useParams` - Access URL parameters
   - `useNavigate` - Programmatic navigation

2. **Full Stack Integration**:
   - Connecting React frontend with Spring Boot backend
   - Making HTTP requests with Axios
   - Handling promises with `.then()` and `.catch()`
   - Managing CORS issues

3. **Modern Development Practices**:
   - Functional components over class components
   - Arrow functions
   - ES6+ JavaScript features
   - RESTful API design
   - DTO pattern for data transfer

### Related Courses by Java Guides

- **Spring Boot + Angular Full Stack**: For Angular developers
- **Spring Boot + Vue.js Full Stack**: For Vue.js developers  
- **Spring Boot Microservices**: Advanced backend development
- **Spring Boot Testing**: JUnit and Mockito
- **Spring Data JPA Mastery**: Deep dive into JPA

### Additional Resources

- [Spring Boot Official Documentation](https://spring.io/projects/spring-boot)
- [React Official Documentation](https://react.dev)
- [React Hooks Documentation](https://react.dev/reference/react)
- [Axios Documentation](https://axios-http.com)
- [React Router Documentation](https://reactrouter.com)
- [Bootstrap Documentation](https://getbootstrap.com)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is created for educational purposes. Feel free to use it for learning and development.

---

## 🙏 Acknowledgments

### Tutorial Creator
- **Ramesh Fadatare** - Founder of [Java Guides](https://www.javaguides.net/)
- YouTube Channel: [Java Guides](https://www.youtube.com/c/javaguides) (178K+ subscribers)
- Tutorial: [Spring Boot + React CRUD Full Stack Tutorial](https://www.javaguides.net/2021/10/spring-boot-react-full-stack-web-development-tutorial.html)

### Technologies & Frameworks
- Spring Boot team for the amazing framework
- React team for the powerful library
- The Spring Data JPA team
- Bootstrap team for the CSS framework
- Axios team for the HTTP client
- MySQL team for the database

### Learning Platform
This project demonstrates the integration of:
- Modern backend development with Spring Boot
- Modern frontend development with React Hooks
- RESTful API design principles
- Full-stack application architecture

### Special Thanks
- The open-source community
- Java Guides for free, high-quality tutorials
- All contributors to the technologies used in this project

---

## 📞 Contact

**Sai Teja Reddy Yeldandi**
- GitHub: [@SaiTejaReddyYeldandi](https://github.com/SaiTejaReddyYeldandi)
- Project Link: [React_Spring_Employment_Management](https://github.com/SaiTejaReddyYeldandi/React_Spring_Employment_Management)

---

## 📝 Important Notes

### Backend Notes

1. **Lombok Usage**: This project uses Lombok to reduce boilerplate code
   - `@Getter` and `@Setter` generate getter/setter methods
   - `@NoArgsConstructor` and `@AllArgsConstructor` generate constructors
   - Don't use `@Data` as it generates unnecessary methods (toString, equals, hashCode)

2. **CORS Configuration**: Required because frontend (port 3000) and backend (port 8080) run on different ports
   ```java
   @CrossOrigin("*")  // Allows all origins
   // Or specify specific origin:
   @CrossOrigin(origins = "http://localhost:3000")
   ```

3. **JPA Configuration**:
   - Use `spring.jpa.hibernate.ddl-auto=update` for development
   - Use `spring.jpa.hibernate.ddl-auto=validate` for production

4. **Exception Handling**: `@ResponseStatus` annotation automatically returns the HTTP status when exception is thrown

### Frontend Notes

1. **React Hooks Rules**:
   - Only call hooks at the top level (not inside loops, conditions, or nested functions)
   - Only call hooks from React functional components
   - `useEffect` with empty dependency array `[]` runs only once on mount

2. **Form Handling**:
   - Use controlled components (value bound to state)
   - Use `onChange` with arrow functions to update state
   - Prevent default form submission with `e.preventDefault()`

3. **Navigation**:
   - Use `<Link>` component for navigation (not `<a>` tags)
   - Use `useNavigate()` hook for programmatic navigation
   - Import from `react-router-dom`

4. **Component Reusability**:
   - Single `EmployeeComponent` handles both Add and Update
   - Check for `id` parameter to determine mode
   - Dynamic page title based on operation

5. **Bootstrap Integration**:
   - Import Bootstrap CSS in `index.js`
   - Use `className` instead of `class` in JSX
   - Use Bootstrap classes: `btn`, `form-control`, `table`, `container`, etc.

### Common Patterns Used

#### 1. Fetch Data on Component Mount
```javascript
useEffect(() => {
    getAllEmployees();
}, [])
```

#### 2. Handle Form Input Changes
```javascript
onChange={(e) => setFirstName(e.target.value)}
```

#### 3. Conditional Rendering
```javascript
{id ? <h2>Update Employee</h2> : <h2>Add Employee</h2>}
```

#### 4. Map Array to JSX
```javascript
{employees.map(employee =>
    <tr key={employee.id}>
        <td>{employee.id}</td>
        <td>{employee.firstName}</td>
    </tr>
)}
```

---

## 🐛 Known Issues & Future Enhancements

### Future Enhancements
- [ ] Add pagination for employee list
- [ ] Implement search and filter functionality
- [ ] Add employee department management
- [ ] Implement authentication and authorization
- [ ] Add employee profile pictures
- [ ] Export employee data to CSV/Excel
- [ ] Add unit and integration tests
- [ ] Deploy to cloud platform (AWS/Heroku)

### Known Issues
- None currently reported

---

## 📊 Database Schema

### Employee Table
```sql
CREATE TABLE employees (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email_id VARCHAR(255)
);
```

---

## 🧪 Testing the Application

### Testing Backend with Postman

#### 1. Get All Employees
```
GET http://localhost:8080/api/v1/employees
```
Expected: Array of employee objects with 200 OK status

#### 2. Get Employee by ID
```
GET http://localhost:8080/api/v1/employees/1
```
Expected: Single employee object with 200 OK status

#### 3. Create Employee
```
POST http://localhost:8080/api/v1/employees
Content-Type: application/json

{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com"
}
```
Expected: Created employee object with 201 Created status

#### 4. Update Employee
```
PUT http://localhost:8080/api/v1/employees/1
Content-Type: application/json

{
    "firstName": "John",
    "lastName": "Smith",
    "email": "john.smith@example.com"
}
```
Expected: Updated employee object with 200 OK status

#### 5. Delete Employee
```
DELETE http://localhost:8080/api/v1/employees/1
```
Expected: 204 No Content status

### Testing Frontend

1. **Access the application**: `http://localhost:3000`
2. **View employees**: Should display list of all employees
3. **Add employee**: Click "Add Employee", fill form, submit
4. **Update employee**: Click "Update" button, modify data, submit
5. **Delete employee**: Click "Delete" button, employee should be removed

### Verification Checklist

- [ ] Backend starts without errors on port 8080
- [ ] Frontend starts without errors on port 3000
- [ ] Database connection is successful
- [ ] `employees` table is created in MySQL
- [ ] Can view all employees in the table
- [ ] Can add new employee successfully
- [ ] Can update existing employee
- [ ] Can delete employee
- [ ] Navigation works between pages
- [ ] Form validation works properly
- [ ] No CORS errors in browser console

---

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Application fails to start
- **Solution**: Verify MySQL is running and credentials in `application.properties` are correct

**Problem**: Port 8080 already in use
- **Solution**: Change the port in `application.properties`:
  ```properties
  server.port=8081
  ```

### Frontend Issues

**Problem**: npm install fails
- **Solution**: Delete `node_modules` and `package-lock.json`, then run `npm install` again

**Problem**: CORS errors
- **Solution**: Ensure `@CrossOrigin("*")` annotation is present in the Controller class

**Problem**: Cannot connect to backend
- **Solution**: Verify backend is running on port 8080 and check the API URL in `EmployeeService.js`

---

## 💡 Tips for Developers

1. **Development Mode**: Use `spring.jpa.hibernate.ddl-auto=create-drop` for development (resets DB on restart)
2. **Production Mode**: Use `spring.jpa.hibernate.ddl-auto=validate` for production
3. **API Testing**: Use Postman or curl to test backend endpoints independently
4. **React DevTools**: Install React Developer Tools browser extension for debugging
5. **Code Organization**: Follow the established package structure for maintainability

---

## ❓ Frequently Asked Questions (FAQ)

### Q1: Why use React Hooks instead of class components?
**A:** React Hooks allow you to use state and other React features in functional components, making code cleaner, more reusable, and easier to understand. They were introduced in React 16.8 and are now the recommended approach.

### Q2: What's the difference between this and the class component version?
**A:** This project uses:
- Functional components with Hooks (useState, useEffect)
- `useNavigate` instead of history object
- `useParams` to access route parameters
- Arrow functions throughout
The class component version would use `this.state`, lifecycle methods like `componentDidMount`, and class syntax.

### Q3: Why do we need CORS configuration?
**A:** CORS (Cross-Origin Resource Sharing) is needed because the React app (port 3000) and Spring Boot API (port 8080) run on different ports. Browsers block these requests by default for security. The `@CrossOrigin("*")` annotation allows the frontend to access the backend.

### Q4: Can I use this with PostgreSQL instead of MySQL?
**A:** Yes! Just:
1. Add PostgreSQL dependency to `pom.xml`
2. Change the datasource URL in `application.properties`
3. Update the dialect to `org.hibernate.dialect.PostgreSQLDialect`

### Q5: How do I deploy this application?
**A:** 
- **Backend**: Build JAR file (`mvn clean package`) and deploy to services like Heroku, AWS, or Railway
- **Frontend**: Build (`npm run build`) and deploy to Netlify, Vercel, or AWS S3
- Update the API base URL in the frontend to point to your deployed backend

### Q6: Why use one component for both Add and Update?
**A:** Code reusability! By checking if an `id` parameter exists in the URL, we can determine whether to create a new employee or update an existing one, reducing code duplication.

### Q7: What if I get "Access to XMLHttpRequest has been blocked by CORS policy" error?
**A:** Make sure:
1. `@CrossOrigin("*")` is added to your controller
2. Spring Boot application is running on port 8080
3. You're making requests to the correct URL

### Q8: Do I need to know Java 17 for this project?
**A:** No, Java 8+ works fine. The project uses Java 11 by default, but you can use Java 8, 11, 17, or later versions.

### Q9: Can I add authentication to this application?
**A:** Yes! You can add Spring Security to the backend and implement JWT-based authentication. This would be a great enhancement to the base project.

### Q10: Where can I get the complete source code?
**A:** Check the [GitHub repository](https://github.com/SaiTejaReddyYeldandi/React_Spring_Employment_Management) for the complete, working code.

---

Made with ❤️ by Sai Teja Reddy Yeldandi | Following Java Guides Tutorial
