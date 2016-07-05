package go_to_ts_py

type StateEnum int32

const (
	StateFoo StateEnum = iota
	StateBar
	StateBaz
)

type FooStruct struct {
	FooString string `json:"my_string,omitempty"`
	FooInt int32 `json:"my_int"`
	FooState StateEnum `json:"my_state"`
}

type BarStruct struct {
	BarString string `json:"my_string"`
	BarInt int32 `json:"my_int,omitempty"`
	BarStates []StateEnum `json:"my_state"`
	BarFoo *FooStruct `json:"my_foo,omitempty"`
}
