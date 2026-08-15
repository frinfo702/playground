const acceptsObj = (obj: { foo: string; bar: number; baz: boolean }) => {};
acceptsObj({
  foo: "uyu",
  bar: 2,
  baz: true,
});

let otherThing = {
  name: "Alice",
};

// expand otherThing
const otherObject = {
  ...otherThing,
  thing: "abc",
};

otherObject.thing;

let element = document.getElementById("12");

/**
 * Logs the values of an object to the console.
 *
 * @param obj - The object to log.
 *
 * @example
 * ```ts
 * logValues({ a: 1, b: 2 });
 * // Output:
 * // a: 1
 * // b: 2
 * ```
 */

function logValues(obj: any) {
  for (const key in obj) {
    console.log(`${key}: ${obj[key]}`);
  }
}

/**
 * return sum of two inputs
 * @param a - number one
 * @prram c - number two
 * @example
 * ```
 * myFunction(a: 1, b:2);
 * ```
 *
 */
const myFunction = (a: number, b: number) => a + b;

const func = () => {
  const randomPercentage = `${(Math.random() * 100).toFixed(2)}%`;

  console.log(randomPercentage);
};

const add = (a: number, b: number) => {
  return a + b;
};

const result = add(1, 2);

type test = Expect<Equal<typeof result, number>>;

const handleFormData = (e: any) => {
  e.preventDefault();

  const data = new FormData(e.terget);

  const value = Object.fromEntries(data.entries());

  return value;
};

it("Should handle a form submit", () => {
  const form = document.createElement("form");

  form.innerHTML = `
<input name="name" value="John Doe"></Exercise>
`;

  form.onsubmit = (e) => {
    const value = handleFormData(e);

    expect(value).toEqual({ name: "John Doe" });
  };

  form.requestSubmit();

  expect.assertions(1);
});
