package go_unit_test_bootcamp

import (
    "math/rand"
    "testing"
    "time"
)

func TestFindMissingDrone_basic(t *testing.T) {
    result := FindMissingDrone([]int{1, 3, 2, 2, 3})

    if result != 1 {
        t.Errorf("expected missing drone ID to be 1, got %d", result)
    }
}

func TestFindMissingDrone_basic2(t *testing.T) {
    result := FindMissingDrone([]int{1, 4, 4, 2, 3, 1, 2})

    if result != 3 {
        t.Errorf("expected missing drone ID to be 3, got %d", result)
    }
}

func TestFindMissingDrone_single(t *testing.T) {
    result := FindMissingDrone([]int{3})

    if result != 3 {
        t.Errorf("expected missing drone ID to be 3, got %d", result)
    }
}

func TestFindMissingDrone_random(t *testing.T) {
    rand.Seed(time.Now().UnixNano())

    missingDrone := rand.Int()
    droneIds := []int{missingDrone}

    for i := 0; i < rand.Intn(20); i++ {
        randomDroneId := rand.Int()
        droneIds = append(droneIds, randomDroneId, randomDroneId)
    }

    rand.Shuffle(len(droneIds), func(i, j int) {
        droneIds[i], droneIds[j] = droneIds[j], droneIds[i]
    })

    result := FindMissingDrone(droneIds)

    if result != missingDrone {
        t.Errorf("expected missing drone ID to be %d, got %d", missingDrone, result)
    }
}
