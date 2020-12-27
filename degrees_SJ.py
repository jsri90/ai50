import csv
import sys

# load names
names = {}

# load people
people = {}

# load movies
movies = {}


def load_data(directory):

# load people
    with open(f"{directory}/people.csv", encoding = "utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            people[row["id"]]={
                "name":row["name"],
                "birth":row["birth"],
                "movies":set()
                }
            if row["name"].lower() not in names:
                names[row["name"].lower()]={row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])
                
    with open(f"{directory}/movies.csv", encoding = "utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            movies[row["id"]] = {
                "title":row["title"],
                "year":row["year"],
                "stars":set()
                }

    with open(f"{directory}/stars.csv", encoding = "utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movie"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass
    
                

def main():
    if len(sys.argv) > 2:
        sys.exit("Usge: python degrees_SJ.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found")

    path = shortest_path(surce, target)

    if path is None:
        print("Not connected")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation")
        path = [(None, source)]+ path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i+1][1]]["name"]
            movie = movies[path[i+1][0]]["title"]
            print(f"{i+1}:{person1} and {person2} starred in {movie}")
                             

def shortest_path(source, target):

    """ Find shortest path between source and target if one exists"""

    # keep track of states explored
    num_explored=0
    start = Node(state=source,parent= None,action= None)
    frontier = QueueFrontier()
    frontier.add(start)

    explored = set()
    

    while True:

        if frontier.empty():
            raise Exception("No solution")

        node = frontier.remove()
        num_explored += 1

        if node.state == target:
            route=[]
            while node.parent is not None:
                route.append((node.action, node.state))
                node = node.parent
            route.reverse()
            return route

        explored.add(node.state)
        expand = neighbors(node.state)
        for m, p in expand:
            if not frontier.contains_state(p) and p not in explored:
                child = Node(state = p, parent = node, action = m)
                frontier.add(child)

                

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """

    person_ids = list(names.get(name.lower(),set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name:{name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID:")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

def neighbors_for_person(person_id):
    """Return (movie_id, person_id) pairs for people
    who starred with a given person.
    """

    movies_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors
    
    
                       




if __name__ == "__main__":
    main()
    for i in movies:
        print(i, movies[i])


    
