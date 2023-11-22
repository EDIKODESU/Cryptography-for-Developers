package main

import (
	"crypto/elliptic"
	"crypto/rand"
	"fmt"
	"math/big"
)

type ECPoint struct {
	X *big.Int
	Y *big.Int
}

func BasePointGGet() (point ECPoint) {
	curve := elliptic.P256()
	return ECPoint{curve.Params().Gx, curve.Params().Gy}
}

func ECPointGen(x, y *big.Int) (point ECPoint) {
	return ECPoint{X: x, Y: y}
}

func IsOnCurveCheck(a ECPoint) (c bool) {
	curve := elliptic.P256()
	return curve.IsOnCurve(a.X, a.Y)
}

func AddECPoints(a, b ECPoint) (c ECPoint) {
	curve := elliptic.P256()
	x, y := curve.Add(a.X, a.Y, b.X, b.Y)
	return ECPoint{X: x, Y: y}
}

func DoubleECPoints(a ECPoint) (c ECPoint) {
	curve := elliptic.P256()
	x, y := curve.Double(a.X, a.Y)
	return ECPoint{X: x, Y: y}
}

func ScalarMult(k *big.Int, a ECPoint) (c ECPoint) {
	curve := elliptic.P256()
	x, y := curve.ScalarMult(a.X, a.Y, k.Bytes())
	return ECPoint{X: x, Y: y}
}

func ECPointToString(point ECPoint) (s string) {
	return fmt.Sprintf("(%s, %s)", point.X.String(), point.Y.String())
}

func StringToECPoint(s string) (point ECPoint) {
	var x, y big.Int
	fmt.Sscanf(s, "(%s, %s)", &x, &y)
	return ECPoint{X: &x, Y: &y}
}

func PrintECPoint(point ECPoint) {
	fmt.Printf("(%s, %s)\n", point.X.String(), point.Y.String())
}

// SetRandom generates a random integer of the specified bit length
func SetRandom(bitLength int) *big.Int {
	random, err := rand.Int(rand.Reader, new(big.Int).Lsh(big.NewInt(1), uint(bitLength)))
	if err != nil {
		panic(err)
	}
	return random
}

// IsEqual checks if two ECPoints are equal
func IsEqual(a, b ECPoint) bool {
	return a.X.Cmp(b.X) == 0 && a.Y.Cmp(b.Y) == 0
}

func main() {
	// Example usage of wrapper functions
	G := BasePointGGet()
	k := SetRandom(256)
	d := SetRandom(256)

	H1 := ScalarMult(d, G)
	H2 := ScalarMult(k, H1)

	H3 := ScalarMult(k, G)
	H4 := ScalarMult(d, H3)

	result := IsEqual(H2, H4)
	fmt.Println("Correctness Check Result:", result)

	// Check is_on_curve_check
	resultOnCurveG := IsOnCurveCheck(G)
	resultOnCurveH1 := IsOnCurveCheck(H1)
	resultOnCurveH2 := IsOnCurveCheck(H2)

	fmt.Println("Is G on curve?", resultOnCurveG)
	fmt.Println("Is H1 on curve?", resultOnCurveH1)
	fmt.Println("Is H2 on curve?", resultOnCurveH2)

	// Check ec_point_gen
	fmt.Println("\nCheck ec_point_gen")
	P := ECPointGen(big.NewInt(123), big.NewInt(456))
	resultOnCurveP := IsOnCurveCheck(P)
	PrintECPoint(P)
	fmt.Println("Is P on curve?", resultOnCurveP)

	M := BasePointGGet()

	// Check add_ec_points
	fmt.Println("\nCheck add_ec_points")
	Q := AddECPoints(G, M)
	resultOnCurveQ := IsOnCurveCheck(Q)
	PrintECPoint(Q)
	fmt.Println("Is Q on curve?", resultOnCurveQ)

	// Check double_ec_points
	fmt.Println("\nCheck double_ec_points")
	R := DoubleECPoints(M)
	resultOnCurveR := IsOnCurveCheck(R)
	PrintECPoint(R)
	fmt.Println("Is R on curve?", resultOnCurveR)

	// Check ec_point_to_string
	fmt.Println("\nCheck ec_point_to_string")
	stringRepresentationP := ECPointToString(M)
	reconstructedP := StringToECPoint(stringRepresentationP)
	resultStringConversion := IsEqual(M, reconstructedP)
	fmt.Println("String conversion result:", resultStringConversion)

	// Check print_ec_point
	fmt.Println("\nCheck print_ec_point")
	fmt.Println("Printed point:")
	PrintECPoint(P)
}
